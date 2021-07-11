import pytest
from flask import url_for
from webtest import TestApp

test_user = {
    'email': 'test_user@email.com',
    'username': 'test_user_fn',
    'password': '111111'
}
URL_USERS = 'user.'


@pytest.fixture(scope='function')
def register_user(testapp: TestApp, **kwargs):
    def _func(**kwargs):
        return testapp.post_json(
            url_for(f'{URL_USERS}register_user'),
            {
                "user": test_user
            },
            **kwargs
        )
    return _func
