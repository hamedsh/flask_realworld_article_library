from marshmallow import Schema, fields


class TagSchema(Schema):
    tag_name = fields.Str()

