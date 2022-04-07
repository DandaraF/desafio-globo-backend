from challenge_app.adapters import CardMongodbAdapter
from challenge_app.domain import Card

import logging


class PostCardException(BaseException):
    pass


class PostCardRequestModel:
    def __init__(self, json_data):
        self.json_data = json_data
        self.json_data['_id'] = ''


class PostCardResponseModel:
    def __init__(self, card_id):
        self.card_id = card_id

    def __call__(self):
        return self.card_id


class PostCardInteractor:
    def __init__(self, adapter: CardMongodbAdapter,
                 request: PostCardRequestModel):
        self.adapter = adapter
        self.request = request
        self.logger = logging.getLogger(__name__)

    def save_card(self, card: Card):
        card.set_adapter(self.adapter)
        return card.save()

    def run(self):
        try:
            card = Card.from_json(self.request.json_data)
            save_result = self.save_card(card)
            response = PostCardResponseModel(save_result)
            return response

        except Exception as e:
            msg = f'Erro durante a criação do card: {e.__class__.__name__}'
            self.logger.error(msg)
            raise PostCardException(msg)
