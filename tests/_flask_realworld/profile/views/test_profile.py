from flask import url_for, Response
from webtest import TestApp

from flask_realworld.exceptions import USER_NOT_FOUND
from tests._flask_realworld.profile.views.conftest import test_user

URL_USERS = 'user.'
URL_PROFILE = 'profile.'


def test_get_user_profile_while_not_logged_in(testapp: TestApp, register_user) -> None:
    register_user()

    response: Response = testapp.get(
        url_for(f'{URL_PROFILE}get_profile', username=test_user['username']),
    )

    assert response.status_code == 200
    assert response.json['profile']['email'] == test_user['email']
    assert not response.json['profile']['following']


def test_get_profile_that_does_not_exist_then_it_return_404(testapp: TestApp) -> None:
    response: Response = testapp.get(
        url_for(f'{URL_PROFILE}get_profile', username=test_user['username']),
        expect_errors=True,
    )

    assert response.status_code == 404
    assert response.json == USER_NOT_FOUND['message']


def test_follow_a_user_then_it_return_following(testapp: TestApp, register_user, user):
    followed_user = user.get()
    register_response: Response = register_user()
    token = register_response.json['user']['token']

    follow_response: Response = testapp.post(
        url_for(f'{URL_PROFILE}follow_user', username=followed_user.username),
        headers={'Authorization': f'Token {token}'}
    )

    assert follow_response.json['profile']['following']


def test_when_unfollow_a_followed_user_then_it_should_not_return_it(
        testapp: TestApp,
        register_user,
        user,
):
    followed_user = user.get()
    register_response: Response = register_user()
    token = register_response.json['user']['token']
    follow_response: Response = testapp.post(
        url_for(f'{URL_PROFILE}follow_user', username=followed_user.username),
        headers={'Authorization': f'Token {token}'}
    )

    unfollow_response: Response = testapp.delete(
        url_for(f'{URL_PROFILE}follow_user', username=followed_user.username),
        headers={'Authorization': f'Token {token}'}
    )

    assert unfollow_response.status_code == 200
    assert not unfollow_response.json['profile']['following']


def test_when_unfollow_an_user_that_is_not_followed_then_it_should_return_empty_list(
        testapp: TestApp,
        register_user,
        user,
):
    followed_user = user.get()
    register_response: Response = register_user()
    token = register_response.json['user']['token']

    unfollow_response: Response = testapp.delete(
        url_for(f'{URL_PROFILE}follow_user', username=followed_user.username),
        headers={'Authorization': f'Token {token}'}
    )

    assert unfollow_response.status_code == 200
    assert not unfollow_response.json['profile']['following']


def test_when_unfollow_an_user_that_is_not_exist_then_it_should_return_empty_list(
        testapp: TestApp,
        register_user,
):
    register_response: Response = register_user()
    token = register_response.json['user']['token']
    follow_response: Response = testapp.post(
        url_for(f'{URL_PROFILE}follow_user', username='not_existed_user'),
        headers={'Authorization': f'Token {token}'},
        expect_errors=True,
    )

    assert follow_response.status_code == 404
    assert not follow_response.json == USER_NOT_FOUND
