from basic_domain import BasicEntity
from marshmallow import fields, post_load
from challenge_app.domain.tag import Tag
from datetime import date
from typing import List


class Card(BasicEntity):
    def __init__(self,
                 text: str,
                 date_creation: date,
                 entity_id: str = None,
                 tags: List[Tag] = None,
                 date_modification: date = None):
        super().__init__(entity_id)
        self.text = text
        self.tags = tags or []
        self.date_creation = date_creation
        self.date_modification = date_modification

    class Schema(BasicEntity.Schema):
        text = fields.Str(required=True,
                          allow_none=False)
        tags = fields.Str(required=False,
                          allow_none=True)
        date_creation = fields.Date(required=True,
                                    allow_none=False)
        date_modification = fields.Date(required=False,
                                        allow_none=True)

        @post_load
        def post_load(self, data, **kwargs):
            return Card(**data)
