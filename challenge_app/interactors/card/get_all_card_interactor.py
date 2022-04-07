from challenge_app.adapters import CardMongodbAdapter
from challenge_app.domain import Card
from typing import List
import logging


class GetAllCardException(BaseException):
    pass


class GetAllCardResponseModel:
    def __init__(self, cards: List[Card]):
        self.cards = cards

    def __call__(self):
        return [x.to_json() for x in self.cards]


class GetAllCardInteractor:
    def __init__(self, card_adapter: CardMongodbAdapter):
        self.card_adapter = card_adapter
        self.logger = logging.getLogger(__name__)

    def run(self):
        try:
            card_list = self.card_adapter.list_all()
            return GetAllCardResponseModel(card_list)

        except Exception as e:
            msg = f'Erro ao obter todos os dados. {e.__class__.__name__}: {e}'
            self.logger.error(msg)
            raise GetAllCardException(msg)
