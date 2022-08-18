from dataclasses import dataclass
from typing import List

from challenge_app.domain import Card


@dataclass
class GetCardsResponseModel:
    cards: List[Card]


class GetCardsInteractor:
    def __init__(self, card_adapter: BasicPersistAdapter):
