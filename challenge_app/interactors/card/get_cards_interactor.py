from dataclasses import dataclass
from typing import List

from challenge_app.adapters import BasicMongodbAdapter
from challenge_app.domain import Card


class GetCardsRequestModel:
    def __init__(self, query_params: dict):
        params = query_params if query_params else {}
        self.tag = params.get('tag')
        self.text = params.get('text')


@dataclass
class GetCardsResponseModel:
    cards: List[Card]


class GetCardsInteractor:
    def __init__(self,
                 request: GetCardsRequestModel,
                 card_adapter: BasicMongodbAdapter):
        self.request = request
        self.card_adapter = card_adapter

    def _criar_filtro(self):
        filtro = dict(tag__begins_with=self.request.tag,
                      text__contains=self.request.text)

        filtro_args = self._remove_nulls(filtro)

        return self.card_adapter.filter(**filtro_args)

    @staticmethod
    def _remove_nulls(filtro: dict):
        return {k: v for k, v in filtro.items() if v}

    def _lista_filtrado(self) -> List[Card]:
        filtro = self._criar_filtro()
        return self.card_adapter.filter(**filtro)

    def _lista_tudo(self) -> List[Card]:
        return self.card_adapter.list_all()

    def _get_cards(self):
        filtrado = self.request.tag or self.request.text
        return self._lista_filtrado() if filtrado else self._lista_tudo()

    def run(self):
        cards: List[Card] = self._get_cards()

        return GetCardsResponseModel(cards)
