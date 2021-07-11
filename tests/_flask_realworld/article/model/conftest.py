import pytest

from flask_realworld.articles.models.article import Article
from flask_realworld.user.models.user import User


@pytest.fixture(scope='function')
def article(db_test, user: User) -> Article:
    user = user.get()
    article = Article(user.profile, 'title', 'some body', description='some')
    article.save()
    return article
