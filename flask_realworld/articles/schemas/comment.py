from marshmallow import Schema, fields, pre_load, post_dump

from flask_realworld.profile.schemas.profile import ProfileSchema


class CommentSchema(Schema):
    created_at = fields.DateTime()
    body = fields.Str()
    updated_at = fields.DateTime(dump_only=True)
    author = fields.Nested(ProfileSchema)

    comment = fields.Nested('self', exclude=('comment', ), default=True, load_only=True)

    @pre_load
    def make_comment(self, data, **kwargs):
        return data['comment']

    @post_dump
    def dump_comment(self, data, **kwargs):
        data['author'] = data['author']['profile']
        return {'comment': data}

    class Meta:
        strict = True


class CommentsSchema(CommentSchema):
    @post_dump
    def dump_comment(self, data, **kwargs):
        data['author'] = data['author']['profile']
        return data

    @post_dump(pass_many=True)
    def make_comment(self, data, many, **kwargs):
        return {'comments': data}
        # todo: add comments count


comment_schema = CommentSchema()
comments_schema = CommentsSchema(many=True)
