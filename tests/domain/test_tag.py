from challenge_app.domain import Tag
from tests.util import generic_serialize_roundtrip_test


def test_tag_roundtrip():
    tag = Tag(name='HISTÓRICO',
              entity_id='1234')

    generic_serialize_roundtrip_test(Tag, tag)

    assert isinstance(tag, Tag)
