"""App module that contains app factory function"""
import os
from typing import Dict, Any, Type

from flask import Flask

from flask_realworld.articles.views.articles import articles_bp
from flask_realworld.articles.views.comments import comments_bp
from flask_realworld.articles.views.tags import tags_bp
from flask_realworld.exceptions import InvalidUsage
from flask_realworld.extensions import db, bcrypt, cache, migrate, jwt
from flask_realworld.profile.views.profile import profile_blueprint
from flask_realworld.settings import DevConfig, TestConfig
from flask_realworld.user.views.user_view import user_blueprint


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_blueprints(app: Flask) -> None:
    # todo: only one blueprint for multiple view
    app.register_blueprint(articles_bp, url_prefix='/api/articles/')
    app.register_blueprint(tags_bp, url_prefix='/api/articles/')
    app.register_blueprint(comments_bp, url_prefix='/api/articles/')

    app.register_blueprint(profile_blueprint, url_prefix='/api/profiles/')
    app.register_blueprint(user_blueprint, url_prefix='/api/user/')


def register_error_handlers(app: Flask) -> None:

    def errorhandler(error) -> object:
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


def register_shellcontext(app: Flask) -> None:
    pass


def register_commands(app: Flask) -> None:
    pass


def create_app(config_project: Type[TestConfig] = DevConfig) -> Flask:
    """
    An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    Args:
        config_project:
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config_project)

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shellcontext(app)
    register_commands(app)

    return app
