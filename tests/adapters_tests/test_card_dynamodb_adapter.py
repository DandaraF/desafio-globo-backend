from unittest.mock import patch

from challenge_app.adapters import CardDynamodbAdapter
from challenge_app.domain import Card


@patch('boto3.client')
@patch('boto3.resource')
def test_card_adapter(resource_mock, client_mock):
    adapter = CardDynamodbAdapter('card')

    assert adapter._table_name == 'card'
    assert adapter._class == Card