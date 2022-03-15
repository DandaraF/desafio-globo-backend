from unittest.mock import patch

from challenge_app.domain import Tag

from challenge_app.adapters import TagDynamodbAdapter


@patch('boto3.client')
@patch('boto3.resource')
def test_tag_adapter(resource_mock, client_mock):
    adapter = TagDynamodbAdapter('tag')

    assert adapter._table_name == 'tag'
    assert adapter._class == Tag
