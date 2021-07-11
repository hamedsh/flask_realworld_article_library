import datetime as dt
from typing import Any, List, Union

from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import current_user, jwt_required
from marshmallow import fields

from flask_realworld.articles.models.article import Article
from flask_realworld.articles.models.tags import Tags
from flask_realworld.articles.schemas.article import articles_schema, article_schema
from flask_realworld.exceptions import InvalidUsage
from flask_realworld.user.models.user import User

articles_bp = Blueprint('articles', __name__)


@articles_bp.route('', methods=('GET', ), endpoint='get_articles')
@jwt_required(optional=True)
@use_kwargs({
    'tag': fields.Str(),
    'author': fields.Str(),
    'favorited': fields.Str(),
    'limit': fields.Int(),
    'offset': fields.Int(),
})
@marshal_with(articles_schema)
def get_articles(tag: str = None, author: str = None, favorited: str = None, limit: int = 20, offset: int = 0) -> Any:
    res = Article.query
    if tag:
        res = res.filter(Article.tag_list.any(Tags.tag_name == tag))
    if author:
        res = res.join(Article.author).join(User).filter(User.username == author)
    if favorited:
        res = res.join(Article.favoriters).filter(User.username == favorited)
    return res.offset(offset).limit(limit).all()


@articles_bp.route('', methods=('POST', ), endpoint='add_article')
@jwt_required()
@use_kwargs(article_schema)
@marshal_with(article_schema)
def add_article(body: str, title: str, description: str, tag_list: List = None) -> "Article":
    article = Article(
        title=title,
        description=description,
        body=body,
        author=current_user.profile,
    )
    if tag_list is not None:
        for tag in tag_list:
            db_tag = Tags.query.filter_by(tag_name=tag).first()
            if not db_tag:
                db_tag = Tags(tag)
                db_tag.save()
            article.add_tag(db_tag)
    article.save()
    return article


@articles_bp.route('<string:slug>', methods=['PUT'], endpoint='update_article')
@jwt_required()
@use_kwargs(article_schema)
@marshal_with(article_schema)
def update_article(slug: str, **kwargs: object) -> Union["Article", InvalidUsage]:
    article = Article.query.filter_by(slug=slug, author_id=current_user.profile.id).first()
    if article is None:
        raise InvalidUsage.article_not_found()
    article.update(update_at=dt.datetime.utcnow(), **kwargs)
    article.save()
    return article


@articles_bp.route('<string:slug>', methods=['DELETE'], endpoint='delete_article')
@jwt_required()
def delete_article(slug: str) -> Union[InvalidUsage, object]:
    article = Article.query.filter_by(slug=slug, author_id=current_user.profile.id).first()
    if article is None:
        raise InvalidUsage.article_not_found()
    article.delete()
    return '', 200


@articles_bp.route('<string:slug>', methods=('GET', ), endpoint='get_article')
@jwt_required(optional=True)
@marshal_with(article_schema)
def get_article(slug: str) -> Union[InvalidUsage, "Article"]:
    article = Article.query.filter_by(slug=slug).first()
    if article is None:
        raise InvalidUsage.article_not_found()
    return article


@articles_bp.route('<slug>/favorite', methods=('POST', ), endpoint='like_article')
@jwt_required()
@marshal_with(article_schema)
def like_article(slug: str) -> Union[InvalidUsage, "Article"]:
    article = Article.query.filter_by(slug=slug).first()
    profile = current_user.profile
    if article is None:  # todo: this sentence is repeated multiple times, it should refactored
        raise InvalidUsage.article_not_found()
    article.favourite(profile)
    return article


@articles_bp.route('<string:slug>/favorite', methods=('DELETE', ), endpoint='unlike_article')
@jwt_required()
@marshal_with(article_schema)
def unlike_article(slug: str) -> Union[InvalidUsage, Article]:
    article = Article.query.filter_by(slug=slug).first()
    profile = current_user.profile
    if article is None:
        raise InvalidUsage.article_not_found()
    article.unfavourite(profile)
    return article


@articles_bp.route('feed', methods=('GET', ), endpoint='articles_feed')
@jwt_required()
@marshal_with(articles_schema)
def articles_feed(limit: int = 20, offset: int = 0) -> List[Article]:
    return Article.query.\
        join(current_user.profile.follows).\
        order_by(Article.created_at.desc()).\
        offset(offset).\
        limit(limit).\
        all()


@articles_bp.route('hello', methods=('GET', ), endpoint='hello')
@jwt_required(optional=True)
def hello():
    return {'hello': 'world'}
