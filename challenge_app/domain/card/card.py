from challenge_app.domain.basic_entity import BasicEntity
from marshmallow import fields, post_load
from challenge_app.domain.tag import Tag
from datetime import date
from typing import List


class Card(BasicEntity):
    def __init__(self,
                 text: str,
                 tags: List[Tag] = None,
                 date_creation: date = None,
                 date_modification: date = None,
                 entity_id: str = None):
        super(Card, self).__init__(entity_id)
        self.text = text
        self.tags = tags
        self.date_creation = date_creation
        self.date_modification = date_modification

        class Schema(BasicEntity.Schema):
            text = fields.String(required=True,
                                 allow_none=False)
            tags = fields.String(required=False,
                                 allow_none=True)
            date_creation = fields.Date(required=True,
                                        allow_none=False)
            date_modification = fields.Date(required=False,
                                            allow_none=True)

            @post_load
            def post_load(self, data, many, partial, **kwargs):
                return Card(**data)
