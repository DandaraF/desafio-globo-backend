from datetime import date

from tests.util import generic_serialize_roundtrip_test
from challenge_app.domain import Card
from challenge_app.domain import Tag


def test_card_roundtrip():
    card = Card(entity_id=None,
                text="Primeira partida",
                tags=[Tag('TEMPORADA'),
                      Tag('HISTÓRICO')],
                date_creation=date(2022, 2, 1),
                date_modification=date(2022, 2, 1))
    generic_serialize_roundtrip_test(Card, card)
