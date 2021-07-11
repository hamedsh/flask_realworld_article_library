import datetime as dt

from flask_jwt_extended import current_user
from slugify import slugify

from flask_realworld.articles.models._favoriter import favoriter_assoc
from flask_realworld.articles.models._tag import tag_assoc
from flask_realworld.database import Model, reference_col, relationship, SurrogatePK, Column
from flask_realworld.extensions import db
from flask_realworld.profile.models.user_profile import UserProfile
# this is a strange behaviour of sqlalchemy
import flask_realworld.articles.models.comment
import flask_realworld.articles.models.tags


class Article(SurrogatePK, Model):
    __tablename__ = 'article'

    slug = Column(db.Text, unique=True)
    title = Column(db.String(100), nullable=False)
    description = Column(db.Text, nullable=False)
    body = Column(db.Text)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    author_id = reference_col('userprofile', nullable=False)
    author = relationship('UserProfile', backref=db.backref('articles'))
    favoriters = relationship(
        'UserProfile',
        secondary=favoriter_assoc,
        backref='favorites',
        lazy='dynamic',
    )

    tag_list = relationship(
        'Tags',
        secondary=tag_assoc,
        backref='articles',
    )

    comments = relationship(
        'Comment',
        backref=db.backref('article'),
        lazy='dynamic',
    )

    def __init__(self, author, title, body, description, slug=None, **kwargs):
        db.Model.__init__(
            self,
            author=author,
            title=title,
            description=description,
            body=body,
            slug=slug or slugify(title),
            **kwargs,
        )

    def favourite(self, profile):
        if not self.is_favourite(profile):
            self.favoriters.append(profile)
            return True
        return False

    def unfavourite(self, profile):
        if self.is_favourite(profile):
            self.favoriters.remove(profile)
            return True
        return False

    def is_favourite(self, profile):
        return bool(self.query.filter(favoriter_assoc.c.favoriter == profile.id).count())

    def add_tag(self, tag):
        if tag not in self.tag_list:
            self.tag_list.append(tag)
            return True
        return False

    def remove_tag(self, tag):
        if tag in self.tag_list:
            self.tag_list.remove(tag)
            return True
        return False

    @property
    def favorites_count(self):
        return len(self.favoriters.all())

    @property
    def favorited(self):
        if current_user:
            profile = current_user.profile
            return self.query.join(Article.favoriters).filter(UserProfile.id == profile.id).count() == 1
        return False
