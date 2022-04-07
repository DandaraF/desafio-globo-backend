from marshmallow import fields, post_load

from challenge_app.domain import BasicEntity
from challenge_app.domain.basic_value import BasicValue


class Tag(BasicEntity):
    def __init__(self,
                 entity_id: str = None,
                 name: str = None):
        super().__init__(entity_id)
        self.entity_id = entity_id
        self.name = name

    class Schema(BasicValue.Schema):
        entity_id = fields.String(required=False,
                                  allow_none=True)
        name = fields.String(required=True,
                             allow_none=False)

        @post_load
        def post_load(self, data, **kwargs):
            return Tag(**data)
