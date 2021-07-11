from typing import Union, List

from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import current_user, jwt_required

from flask_realworld.articles.models.article import Article
from flask_realworld.articles.models.comment import Comment
from flask_realworld.articles.schemas.comment import comments_schema, comment_schema
from flask_realworld.exceptions import InvalidUsage

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('<int:article_id>/comments', methods=('GET', ), endpoint='get_comments')
@marshal_with(comments_schema)
def get_comments(article_id: int) -> Union[InvalidUsage, List[Comment]]:
    article = Article.query.filter(article_id=article_id).first()
    if article is None:
        raise InvalidUsage.article_not_found()
    return article.comments


@comments_bp.route('<int:article_id>/comments', methods=('POST', ), endpoint='add_comment')
@jwt_required()
@use_kwargs(comment_schema)
@marshal_with(comment_schema)
def add_comment(article_id: int, body, **kwargs) -> Union[InvalidUsage, List[Comment]]:
    article = Article.query.filter(article_id=article_id).first()
    if article is None:
        raise InvalidUsage.article_not_found()
    comment = Comment(article, current_user.profile, body, **kwargs)
    comment.save()
    return comment


@comments_bp.route(
    '<int:article_id>/comments/<int:comment_id>',
    methods=('DELETE', ),
    endpoint='delete_comment',
)
@jwt_required()
def delete_comment(article_id: int, comment_id: int) -> object:
    article = Article.query.filter(article_id=article_id).first()
    if article is None:
        raise InvalidUsage.article_not_found()
    comment = Comment.query.filter_by(id=comment_id, author=current_user.profile).first()
    comment.delete()
    return '', 200
    # todo: verify return codes
