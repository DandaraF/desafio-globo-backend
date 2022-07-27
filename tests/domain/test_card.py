from datetime import date

from challenge_app.domain import Card, Tag
from tests.util import generic_serialize_roundtrip_test


def test_card_roundtrip():
    tag = Tag(name='TEMPORADA',
              entity_id='123')

    card = Card(text='text',
                date_creation=date(2020, 6, 23),
                entity_id=None,
                tags=[tag],
                date_modification=date(2020, 7, 23))

    generic_serialize_roundtrip_test(Card, card)

    assert isinstance(card, Card)
