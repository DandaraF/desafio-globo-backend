from unittest import TestCase
from unittest.mock import MagicMock

from challenge_app.interactors.card import (GetCardsResponseModel,
                                            GetCardsInteractor,
                                            GetCardsRequestModel)


def prefixed(text):
    return f'challenge_app.interactors.card.get_cards_interactor.{text}'


class TestGetCardsRequestModel:
    def test_request_model_instance(self):
        query_params = {'text': 'Brasil',
                        'tag': "TEMPORADA"}

        request = GetCardsRequestModel(query_params)

        assert request.tag == query_params["tag"]
        assert request.text == query_params["text"]


class TestGetCardsResponseModel:
    def test_response_model(self):
        mock_card = MagicMock()

        response = GetCardsResponseModel(mock_card)

        assert response.cards == mock_card

class TestGetCardsInteractor:
    def test


