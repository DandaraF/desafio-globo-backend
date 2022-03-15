from .basic_dynamodb_adapter import BasicDynamodbAdapter
from challenge_app.domain.card import Card


class CardDynamodbAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name):
        super().__init__(table_name, None, Card)
