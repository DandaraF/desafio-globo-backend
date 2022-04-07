from challenge_app.domain import Tag
from tests.util import generic_serialize_roundtrip_test


def test_tag_roundtrip():
    tag = Tag(entity_id=None,
              name="TEMPORADA")
    generic_serialize_roundtrip_test(Tag, tag)
