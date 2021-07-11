from flask import Blueprint
from flask_apispec import marshal_with
from flask_jwt_extended import jwt_required, current_user

from flask_realworld.exceptions import InvalidUsage
from flask_realworld.profile.schemas.profile import profile_schema
from flask_realworld.user.models.user import User

ENDPOINT_PREFIX = 'profile'
profile_blueprint = Blueprint('profile', __name__)


@profile_blueprint.route('<username>', methods=('GET',), endpoint='get_profile')
@jwt_required(optional=True)
@marshal_with(profile_schema)
def get_profile(username: str):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise InvalidUsage.user_not_found()
    return user.profile


@profile_blueprint.route('<username>/follow', methods=('POST',), endpoint='follow_user')
@jwt_required()
@marshal_with(profile_schema)
def follow_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise InvalidUsage.user_not_found()
    current_user.profile.follow(user.profile)
    current_user.profile.save()
    return user.profile


@profile_blueprint.route('<username>/follow', methods=('DELETE',), endpoint='unfollow_user')
@jwt_required()
@marshal_with(profile_schema)
def unfollow_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise InvalidUsage.user_not_found()
    current_user.profile.unfollow(user.profile)
    current_user.profile.save()
    return user.profile
