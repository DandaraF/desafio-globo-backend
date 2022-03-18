from marshmallow import fields, post_load

from challenge_app.domain.basic_value import BasicValue

from typing import Optional


class Tag(BasicValue):
    def __init__(self,
                 name: str = None,
                 entity_id: Optional[str] = None, ):
        super(Tag, self).__init__()
        self.name = name
        self.entity_id = entity_id

        class Schema(BasicValue.Schema):
            entity_id = fields.String(required=False,
                                      allow_none=True)
            name = fields.String(required=True,
                                 allow_none=False)

            @post_load
            def post_load(self, data, many, partial):
                return Tag(**data)
