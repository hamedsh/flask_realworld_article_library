import pytest
from flask import url_for
from webtest import TestApp

from flask_realworld.user.models.user import User


@pytest.fixture(scope='function')
def login_token(testapp: TestApp, user: User) -> str:
    URL_USERS = 'user.'
    user = user.get()
    response = testapp.post_json(
        url_for(f'{URL_USERS}login'),
        {
            'user': {
                'email': user.email,
                'password': '111111'
            }
        }
    )
    token = str(response.json['user']['token'])
    return token


@pytest.fixture(scope='function')
def add_article(testapp: TestApp):
    def _func(login_token: str, expect_errors: bool = False):
        URL_ARTICLES = 'articles.'
        add_article_resp = testapp.post_json(
            url_for(f'{URL_ARTICLES}add_article'),
            {
                "article": {
                    "title": "article 1",
                    "description": "article 1 desc",
                    "body": "article 1 body",
                    "tag_list": ["tag1", "tag2", "tag3"]
                }
            },
            headers={"Authorization": f'Token {login_token}'},
            expect_errors=expect_errors,
        )
        return add_article_resp
    return _func
