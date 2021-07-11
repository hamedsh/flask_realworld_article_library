# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask_realworld.user.models.user import User


def jwt_identity(_jwt_header, jwt_data):
    return User.get_by_id(jwt_data['sub'])


def identity_loader(user):
    return user.id
