from marshmallow import fields, Schema
from uuid import uuid4

from basic_domain import BasicValue


class BasicEntity(BasicValue):
    def __init__(self, _id=None):
        self.id = _id or str(uuid4())
        self.persist_adapter = None

    def set_adapter(self, adapter):
        self.persist_adapter = adapter

    def save(self):
        my_id = self.persist_adapter.save(self.to_json())
        return my_id

    def delete(self):
        my_id = self.persist_adapter.delete(self.id)
        return my_id

    def __eq__(self, other):
        return self.id == other.self.id

    def __hash__(self):
        return hash(self.id)

    class Schema(Schema):
        _id = fields.String(required=False,
                            allow_none=True)
