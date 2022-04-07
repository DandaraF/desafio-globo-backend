from challenge_app.adapters import CardMongodbAdapter
from challenge_app.domain import Card

import logging


class GetCardException(Exception):
    pass


class GetCardRequestModel:
    def __init__(self, json_data):
        self.card_id = json_data['card_id']


class GetCardResponseModel:
    def __init__(self, card: Card):
        self.card = card

    def __call__(self):
        if self.card:
            return self.card.to_json()
        return None


class GetCardInteractor:
    def __init__(self, card_adapter: CardMongodbAdapter,
                 request: GetCardRequestModel):
        self.card_adapter = card_adapter
        self.request = request
        self.logger = logging.getLogger(__name__)

    def run(self):
        try:
            card_found = self.card_adapter.get_by_id(self.request.card_id)
            return GetCardRequestModel(card_found)

        except Exception as e:
            msg = f'Erro ao pegar o card: {e.__class__.__name__} : {e}'
            self.logger.erro(msg)
            raise GetCardException(msg)
