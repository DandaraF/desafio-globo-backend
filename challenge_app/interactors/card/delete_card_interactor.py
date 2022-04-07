from challenge_app.adapters import CardMongodbAdapter


class DeleteCardException(BaseException):
    pass


class CardNotExistsException(BaseException):
    pass


class DeleteCardRequestModel:
    def __init__(self, json_data):
        self.card_id = json_data['card_id']


class DeleteCardResponseModel:
    def __init__(self, deleted_id):
        self.deleted_id = deleted_id

    def __call__(self):
        return self.deleted_id


class DeleteCardInteractor:
    def __init__(self, adapter: CardMongodbAdapter,
                 request: DeleteCardRequestModel):
        self.adapter = adapter
        self.request = request

    def check_if_card_exists(self):
        card = self.adapter.get_by_id(self.request.card_id)
        if not card:
            msg = f'Card {self.request.card_id} não existe.'
            raise CardNotExistsException(msg)

    def run(self):
        try:
            self.check_if_card_exists()
            delete_result = self.adapter.delete(self.request.card_id)
            return DeleteCardResponseModel(delete_result)

        except Exception as e:
            msg = f'Erro ao excluir o card: {e.__class__.__name__}: {e}'
            self.logger.error(msg)
            raise DeleteCardException(msg)
