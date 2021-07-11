import pytest
from flask import url_for
from webtest import TestApp

from flask_realworld.app import create_app
from flask_realworld.profile.models.user_profile import UserProfile
from flask_realworld.settings import TestConfig
from flask_realworld.database import db as _db
from flask_realworld.user.models.user import User
from tests._flask_realworld.factories import UserFactory


@pytest.fixture(scope='function')
def app_test():
    _app = create_app(TestConfig)

    with _app.app_context():
        _db.create_all()

    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app_test):
    return TestApp(app_test)


@pytest.fixture(scope='function')
def db_test(app_test):
    _db.app = app_test
    with app_test.app_context():
        _db.create_all()
    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture(scope='function')
def user(db_test) -> "User":
    class User:
        def get(self):
            muser = UserFactory(password='111111')
            UserProfile(muser).save()
            db_test.session.commit()
            return muser
    return User()

