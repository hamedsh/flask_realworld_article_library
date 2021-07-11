from marshmallow import Schema, fields, pre_load, post_dump

from flask_realworld.profile.schemas.profile import ProfileSchema


class ArticleSchema(Schema):
    slug = fields.Str()
    title = fields.Str()
    description = fields.Str()
    body = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    author = fields.Nested(ProfileSchema)
    article = fields.Nested('self', exclude=('article',), default=True, load_only=True)
    tag_list = fields.List(fields.Str())
    favorites_count = fields.Int(dump_only=True)
    favorited = fields.Bool(dump_only=True)

    @pre_load
    def make_article(self, data, **kwargs) -> dict:
        return data['article']

    @post_dump
    def dump_article(self, data, **kwargs) -> dict:
        data['author'] = data['author']['profile']
        return {'article': data}

    class Meta:
        strict = True


class ArticlesSchema(ArticleSchema):
    @post_dump
    def dump_article(self, data, **kwargs) -> dict:
        data['author'] = data['author']['profile']
        return data

    @post_dump(pass_many=True)
    def dump_articles(self, data, many, **kwargs) -> dict:
        return {'articles': data, 'articles_count': len(data)}


article_schema = ArticleSchema()
articles_schema = ArticlesSchema(many=True)
