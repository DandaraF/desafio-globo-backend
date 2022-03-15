from functools import reduce
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Attr

# noinspection PyPackageRequirements
from botocore.exceptions import ClientError

from challenge_app.adapters.basic_persist_adapter import BasicPersistAdapter


class NotExistsException(BaseException):
    pass


class BasicDynamodbAdapter(BasicPersistAdapter):
    def __init__(self, table_name, db_endpoint, adapted_class, logger=None):

        super().__init__(adapted_class, logger)
        self._table_name = table_name
        self._db_endpoint = db_endpoint
        self._db = self._get_db()
        self._table = self._get_table()

        self._create_table_if_dont_exists()

    def _do_table_exists(self):
        existing_tables = boto3.client(
            'dynamodb', endpoint_url=self._db_endpoint).list_tables()
        return self._table_name in existing_tables['TableNames']

    def _create_table_if_dont_exists(self):
        if not self._do_table_exists():
            self.logger.info(f'Creating not existent table {self._table_name}')

            table = self._db.create_table(
                TableName=self._table_name,
                KeySchema=[
                    {
                        'AttributeName': 'entity_id',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'entity_id',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }

            )

            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(
                TableName=self._table_name)

    def _get_db(self):
        return boto3.resource('dynamodb', endpoint_url=self._db_endpoint)

    def _get_table(self):
        return self._db.Table(self._table_name)

    def _instantiate_object(self, x):
        obj = self._class.from_json(x)
        obj.set_adapter(self)
        return obj

    def list_all(self):
        response = self._scan()
        objects = [self._instantiate_object(x) for x in response['Items']]
        return objects

    def get_by_id(self, item_id):
        response = self._table.get_item(key=dict(entity_id=item_id),
                                        ConsistentRead=True)
        if 'Item' in response:
            return self._instantiate_object(response['Item'])
        else:
            return None

    def _check_if_exists(self, item_id):
        item = self.get_by_id(item_id)
        if not item:
            raise NotExistsException(f"Item {item_id} does not exist.")

    @staticmethod
    def _clean_set_empty_elements(arg):
        arg = set(x for x in arg if not hasattr(x, '__len__') or len(x) > 0)
        return arg

    @staticmethod
    def _clean_list_empty_elements(arg):
        result = []
        for value in arg:
            clean_value = BasicDynamodbAdapter._normalize_nodes(value)
            if clean_value:
                result.append(clean_value)
        return result

    @staticmethod
    def _clean_dict_empty_elements(arg):
        result = {}
        for key, value in arg.items():
            clean_value = BasicDynamodbAdapter._normalize_nodes(value)
            if clean_value:
                result.update({key: clean_value})
            return result

    @staticmethod
    def _normalize_nodes(arg):
        cleaners = {set: BasicDynamodbAdapter._clean_set_empty_elements,
                    list: BasicDynamodbAdapter._clean_list_empty_elements,
                    dict: BasicDynamodbAdapter._clean_dict_empty_elements}
        arg_type = type(arg)
        if arg_type in cleaners:
            return cleaners[arg_type](arg)

        if not hasattr(arg, '__len__') or len(arg) != 0:
            return arg
        else:
            return None

    def save(self, json_data):
        entity_id = json_data.get('entity_id', str(uuid4()))
        json_data.update(dict(entity_id=entity_id))
        self.logger.debug(f'Data received to save: {json_data}')
        cleaned_data = BasicDynamodbAdapter._normalize_nodes(json_data)
        self.logger.debug(f'Saving after remove empties: {json_data}')
        self._table.put_item(item=cleaned_data)
        return entity_id

    def delete(self, entity_id):
        try:
            self._table.delete_item(key=dict(entity_id=entity_id))
        except ClientError as e:
            error = e.response['Error']['Message']
            self._logger.error(f'Erro deletando de {self._class.__name__}:'
                               f'{error}')
            return None
        return entity_id

    @staticmethod
    def _get_ops():
        return {'begins_with': 1,
                'between': 2,
                'contains': 1,
                'eq': 1,
                'exists': 0,
                'gt': 1,
                'gte': 1,
                'is_in': 1,
                'lt': 1,
                'lte': 1,
                'ne': 1,
                'not_exists': 0,
                'size': 0}

    @staticmethod
    def _args_from_value(value, arg_count):
        args = []
        if arg_count == 1:
            args.append(value)
        elif arg_count > 1:
            args.extend(value)

        return args

    @staticmethod
    def _get_scan_kwargs(filter_cond, projection_expression):
        scan_kwargs = {
            'FilterExpression': filter_cond
        }
        if projection_expression is not None:
            scan_kwargs.update({
                'ProjectionExpression': projection_expression
            })
        else:
            scan_kwargs.update({
                'Select': 'ALL_ATTRIBUTES'
            })
        return scan_kwargs

    @staticmethod
    def _get_argcount(op, ops):
        try:
            return ops[op]
        except KeyError:
            raise ValueError(f'Comparador inválido: {op}')

    @staticmethod
    def _parse_conditions(args, kwargs):
        ops = BasicDynamodbAdapter._get_ops()
        conditions = list(args)

        for k, v in kwargs.items():
            field, op = k.split('__')
            arg_count = BasicDynamodbAdapter._get_argcount(op, ops)

            args = BasicDynamodbAdapter._args_from_value(v, arg_count)
            field = field.replace('_dot_', '.')
            conditions.append(getattr(Attr(field), op)(*args))

        if not conditions:
            raise ValueError('Nenhuma condição no filtro.')

        return conditions

    @staticmethod
    def filter_and(*args, **kwargs):
        pargs = args
        conditions = BasicDynamodbAdapter._parse_conditions(pargs, kwargs)
        return reduce(lambda accum, curr: accum & curr, conditions)

    @staticmethod
    def filter_or(*args, **kwargs):
        pargs = args
        conditions = BasicDynamodbAdapter._parse_conditions(pargs, kwargs)
        return reduce(lambda accum, curr: accum | curr, conditions)

    @staticmethod
    def _get_conditions(args, kwargs):
        conditions = BasicDynamodbAdapter._parse_conditions(args, kwargs)
        return reduce(lambda accum, curr: accum | curr, conditions)

    def _deserialize(self, result):
        objects = [self._instantiate_object(x) for x in result]
        for obj in objects:
            obj.set_adapter(self)
        return objects

    @staticmethod
    def _extract_projection_expression(kwargs):
        return kwargs.pop('ProjectionExpression', None)

    def filter(self, *args, **kwargs):
        projection_expression = self._extract_projection_expression(kwargs)
        conditions = self._get_conditions(args, kwargs)
        scan_kwargs = self._get_scan_kwargs(conditions, projection_expression)
        result = self._scan(**scan_kwargs)['Items']

        if projection_expression is not None:
            return result

        return self._deserialize(result)

    def _scan(self, **kwargs):
        result = {'Items': []}
        scan_kwargs = kwargs
        while True:
            response = self._table.scan(**kwargs)

            result['Items'].extend(response['Items'])

            if 'LastEvaluatedKey' not in response:
                break

            scan_kwargs.update(
                {'ExclusiveStartKey': response['LastEvaluatedKey']})

            return result
