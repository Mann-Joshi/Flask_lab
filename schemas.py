from marshmallow import Schema, fields

class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class ProductSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

class ProductUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
