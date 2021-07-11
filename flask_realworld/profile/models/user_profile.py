from flask_jwt_extended import current_user

from flask_realworld.database import Model, SurrogatePK, reference_col, relationship
from flask_realworld.extensions import db
from flask_realworld.profile.models._followers import followers_assoc


class UserProfile(Model, SurrogatePK):
    __tablename__ = 'userprofile'

    id = db.Column(db.Integer, primary_key=True)

    user_id = reference_col('users', nullable=False)
    user = relationship('User', backref=db.backref('profile', uselist=False))
    follows = relationship(
        'UserProfile',
        secondary=followers_assoc,
        primaryjoin=id == followers_assoc.c.follower,
        secondaryjoin=id == followers_assoc.c.followed_by,
        backref='followed_by',
        lazy='dynamic',
    )

    def __init__(self, user, **kwargs):
        db.Model.__init__(self, user=user, **kwargs)

    def is_following(self, profile):
        return bool(self.follows.filter(followers_assoc.c.followed_by == profile.id).count())

    def follow(self, profile):
        if self is not profile and not self.is_following(profile):
            self.follows.append(profile)
            return True
        return False

    def unfollow(self, profile):
        if self is not profile and self.is_following(profile):
            self.follows.remove(profile)
            return True
        return False

    @property
    def following(self):
        if current_user:
            return current_user.profile.is_following(self)
        return False

    @property
    def username(self):
        return self.user.username

    @property
    def bio(self):
        return self.user.bio

    @property
    def image(self):
        return self.user.image

    @property
    def email(self):
        return self.user.email
