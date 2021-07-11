from marshmallow import Schema, fields, pre_load, post_dump


class UserSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    password = fields.Str(load_only=True)
    bio = fields.Str()
    image = fields.Url()
    token = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user = fields.Nested('user', exclude=('user', ), default=True, load_only=True)

    @pre_load
    def make_user(self, data: dict, **kwargs) -> dict:
        data = data['user']
        if not data.get('email', True):
            del data['email']
        if not data.get('image', True):
            del data['image']
        return data

    @post_dump
    def dump_user(self, data: dict, **kwargs) -> dict:
        return {'user': data}

    class Meta:
        strict = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)
