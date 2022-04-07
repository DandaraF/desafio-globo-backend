from marshmallow import fields, Schema
from uuid import uuid4

from challenge_app.domain.basic_value import BasicValue


class BasicEntity(BasicValue):
    def __init__(self, entity_id):
        self.entity_id = entity_id or str(uuid4())
        self.persist_adapter = None

    def set_adapter(self, adapter):
        self.persist_adapter = adapter

    def save(self):
        my_id = self.persist_adapter.save(self.to_json())
        return my_id

    def delete(self):
        my_id = self.persist_adapter.delete(self.entity_id)
        return my_id

    def __eq__(self, other):
        return self.entity_id == other.entity_id

    def __hash__(self):
        return hash(self.entity_id)

    class Schema(Schema):
        entity_id = fields.String(required=False,
                                  allow_none=True)
