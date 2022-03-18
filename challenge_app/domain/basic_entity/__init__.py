from marshmallow import fields, Schema
from uuid import uuid4

from challenge_app.domain.basic_value import BasicValue


class BasicEntity(BasicValue):
    def __init__(self, _id=None):
        self._id = _id or str(uuid4())
        self.persist_adapter = None

    def set_adapter(self, adapter):
        self.persist_adapter = adapter

    def save(self):
        my_id = self.persist_adapter.save(self.to_json())
        return my_id

    def delete(self):
        my_id = self.persist_adapter.delete(self._id)
        return my_id

    def __eq__(self, other):
        return self._id == other._id

    def __hash__(self):
        return hash(self._id)

    class Schema(Schema):
        _id = fields.String(required=True, allow_none=True)
