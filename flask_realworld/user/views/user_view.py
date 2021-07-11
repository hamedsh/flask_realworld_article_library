from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import create_access_token, jwt_required, current_user
from sqlalchemy.exc import IntegrityError

from flask_realworld.exceptions import InvalidUsage
from flask_realworld.extensions import db
from flask_realworld.profile.models.user_profile import UserProfile
from flask_realworld.user.models.user import User
from flask_realworld.user.schemas.user import user_schema

ENDPOINT_PREFIX = 'user'
user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('', methods=('POST', ), endpoint='register_user')
@use_kwargs(user_schema)
@marshal_with(user_schema)
def register_user(username: str, password: str, email: str, **kwargs):
    try:
        userprofile = UserProfile(User(username, email, password, **kwargs).save()).save()
        userprofile.user.token = create_access_token(identity=userprofile.user)
    except IntegrityError:
        db.session.rollback()
        raise InvalidUsage.user_already_registered()
    return userprofile.user


@user_blueprint.route('login', methods=('POST', ), endpoint='login')
@jwt_required(optional=True)
@use_kwargs(user_schema)
@marshal_with(user_schema)
def login_user(email, password, **kwargs):
    user = User.query.filter_by(email=email).first()
    if user is not None and user.check_password(password):
        user.token = create_access_token(identity=user, fresh=True)
        return user
    else:
        raise InvalidUsage.user_not_found()


@user_blueprint.route('', methods=('GET',), endpoint='get_user')
@jwt_required()
@marshal_with(user_schema)
def get_user():
    user = current_user
    # Not sure about this
    user.token = request.headers.environ['HTTP_AUTHORIZATION'].split('Token ')[1]
    return current_user


@user_blueprint.route('', methods=('PUT',), endpoint='update_user')
@jwt_required()
@use_kwargs(user_schema)
@marshal_with(user_schema)
def update_user(**kwargs):
    user = current_user
    # take in consideration the password
    password = kwargs.pop('password', None)
    if password:
        user.set_password(password)
    if 'updated_at' in kwargs:
        kwargs['updated_at'] = user.created_at.replace(tzinfo=None)
    user.update(**kwargs)
    return user
