from marshmallow import fields, post_load

from app.domain.basic_entity import BasicEntity


class Tag(BasicEntity):
    def __init__(self,
                 name: str = None,
                 _id: str = None):
        super(Tag, self).__init__(_id=_id)
        self.name = name

        class Schema(BasicEntity.Schema):
            name = fields.String(required=True,
                                 allow_none=False)

            @post_load
            def post_load(self, data, many, partial, **kwargs):
                return Tag(**data)
