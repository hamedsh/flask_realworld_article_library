import pytest
from flask import url_for, Response
from webtest import TestApp

from flask_realworld.user.schemas.user import UserSchema

URL_ARTICLES = 'articles.'
URL_USERS = 'user.'


def test_when_user_is_logged_id_and_an_article_added_for_a_user_then_number_of_articles_increased(
        testapp: TestApp,
        user: object,
) -> None:
    user: UserSchema = user.get()
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
    for article_num in range(2):
        testapp.post_json(
            url_for(f'{URL_ARTICLES}add_article'),
            {
                "article": {
                    "title": f"article {article_num}",
                    "description": f"description for article {article_num}",
                    "body": f"body of article {article_num}",
                    "tag_list": ["tag1", "tag2", "tag3"]
                }
            },
            headers={
                'Authorization': f'Token {token}'
            }
        )

    subject = testapp.get(
        url_for(f'{URL_ARTICLES}get_articles', author=user.username),
    )

    assert len(subject.json['articles']) == 2


def test_when_user_not_logged_in_then_it_refuse_add_article(
        testapp: TestApp,
        add_article,
) -> None:
    response: Response = add_article(login_token='fake_token', expect_errors=True)
    assert 422 == response.status_code

    subject = testapp.get(
        url_for(f'{URL_ARTICLES}get_articles'),
    )

    assert len(subject.json['articles']) == 0


def test_when_an_user_like_an_article_then_it_returns_as_favirietes(
        testapp: TestApp,
        user: UserSchema,
        login_token,
        add_article,
) -> None:
    add_article_response = add_article(login_token)

    subject = testapp.post(
        url_for(f'{URL_ARTICLES}like_article', slug=add_article_response.json['article']['slug']),
        headers={"Authorization": f'Token {login_token}'}
    )

    assert subject.json['article']['favorited']


def test_when_we_update_an_article_then_it_return_updated_version(
        testapp: TestApp,
        user: UserSchema,
        login_token,
        add_article,
):
    expected_article_title = 'updated article'
    add_article_response = add_article(login_token)
    article = add_article_response.json['article']
    article['title'] = 'updated title'

    update_response = testapp.put_json(
        url_for(f'{URL_ARTICLES}update_article', slug=article['slug']),
        {
            "article": {
                "title": expected_article_title,
                "description": "article 1 desc",
                "body": "article 1 body"
            }
        },
        headers={"Authorization": f'Token {login_token}'},
    )

    updated_article = testapp.get(
        url_for(f'{URL_ARTICLES}get_article', slug=article['slug']),
        headers={"Authorization": f'Token {login_token}'},
    )

    assert updated_article.json['article']['title'] == expected_article_title
