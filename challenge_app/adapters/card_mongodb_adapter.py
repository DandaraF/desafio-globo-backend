from .basic_mongodb_adapter import BasicMongodbAdapter
from challenge_app.domain.card import Card


class CardMongodbAdapter(BasicMongodbAdapter):
    def __init__(self, table_name: str,
                 db_name: str,
                 db_url: str,
                 db_username: str,
                 db_password: str):
        super(CardMongodbAdapter, self).__init__(table_name=table_name,
                                                 db_name=db_name,
                                                 db_url=db_url,
                                                 db_username=db_username,
                                                 db_password=db_password,
                                                 adapted_class=Card)
