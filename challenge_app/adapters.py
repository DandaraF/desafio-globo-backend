from challenge_app.adapters import (CardDynamodbAdapter, TagDynamodbAdapter)

from challenge_app.settings import Settings


def get_card_adapter():
    return CardDynamodbAdapter(Settings.CARD_TABLE_NAME)


def get_tag_adapter():
    return TagDynamodbAdapter(Settings.TAG_TABLE_NAME)
