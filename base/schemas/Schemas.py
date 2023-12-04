from marshmallow import Schema, fields

class userSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)

class categorySchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    user_id = fields.String(required=False)

    
class recordSchema(Schema):
    id = fields.UUID(dump_only=True)
    user_id = fields.UUID(required=True)
    category_id = fields.UUID(required=True)
    created_at = fields.DateTime(dump_only=True)
    amount = fields.Float(required=True)