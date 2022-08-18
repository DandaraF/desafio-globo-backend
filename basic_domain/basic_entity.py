from marshmallow import fields, Schema
from uuid import uuid4

from basic_domain import BasicValue


class BasicEntity(BasicValue):
    def __init__(self, entity_id):
        self.entity_id = entity_id or str(uuid4())
        self.adapter = None

    def set_adapter(self, adapter):
        self.adapter = adapter

    def save(self):
        my_id = self.adapter.save(self.to_json())
        return my_id

    def delete(self):
        my_id = self.adapter.delete(self.entity_id)
        return my_id

    def __eq__(self, other):
        return self.entity_id == other.entity_id

    def __hash__(self):
        return hash(self.entity_id)

    class Schema(Schema):
        entity_id = fields.String(required=False,
                                  allow_none=True)
