from marshmallow import fields, post_load

from challenge_app.domain import BasicEntity


class Tag(BasicEntity):
    def __init__(self,
                 name: str,
                 entity_id: str = None):
        super().__init__(entity_id)
        self.name = name

    class Schema(BasicEntity.Schema):
        name = fields.Str(required=True,
                          allow_none=False)

        @post_load
        def post_load(self, data, **kwargs):
            return Tag(**data)
