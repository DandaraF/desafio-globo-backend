from .basic_dynamodb_adapter import BasicDynamodbAdapter
from app.domain.tag import Tag


class TagDynamodbAdapter(BasicDynamodbAdapter):
    def __init__(self,
                 table_name: str,
                 db_name: str,
                 db_url: str,
                 db_username: str,
                 db_password: str):
        super(TagDynamodbAdapter, self).__init__(table_name=table_name,
                                                 db_name=db_name,
                                                 db_url=db_url,
                                                 db_username=db_username,
                                                 db_password=db_password,
                                                 adapted_class=Tag)
