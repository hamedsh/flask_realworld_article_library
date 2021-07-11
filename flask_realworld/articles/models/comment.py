import datetime as dt

from flask_realworld.database import Model, reference_col, relationship, Column, SurrogatePK
from flask_realworld.extensions import db


class Comment(Model, SurrogatePK):
    __tablename__ = 'comment'

    body = Column(db.Text)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    author_id = reference_col('userprofile', nullable=False)
    author = relationship('UserProfile', backref=db.backref('comments'))
    article_id = reference_col('article', nullable=False)

    def __init__(self, article, author, body: str, **kwargs) -> None:
        db.Model.__init__(self, author=author, body=body, article=article, **kwargs)
