import logging
from typing import List

from challenge_app.adapters.card_adapter import CardAdapter
from challenge_app.domain import Card


class GetAllCardsException(BaseException):
    ...


class GetAllCardsResponseModel:
    def __init__(self, cards: List[Card]):
        self.cards = cards

    def __call__(self):
        return [x.to_json() for x in self.cards]


class GetAllCardsInteractor:
    def __init__(self, card_adapter: CardAdapter):
        self.card_adapter = card_adapter
        self.logger = logging.getLogger(__name__)

    def run(self):

        try:
            card_list = self.card_adapter.list_all()
            return GetAllCardsResponseModel(card_list)

        except Exception as e:
            msg = 'Erro durante a listagem dos cards: ' \
                  f'{e.__class__.__name__}: {e}'
            raise GetAllCardsException(msg)
