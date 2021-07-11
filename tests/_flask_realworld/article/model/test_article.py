from flask_realworld.articles.models.article import Article
from flask_realworld.articles.models.tags import Tags
from flask_realworld.profile.models.user_profile import UserProfile
from flask_realworld.user.models.user import User


def test_when_create_an_article_with_author_then_it_return_correct_author(db_test, user) -> None:
    user = user.get()

    article: Article = Article(user.profile, 'title', 'body', description='description')
    article.save()

    assert article.author.user == user


def test_when_like_an_article_then_it_return_them(db_test) -> None:
    user: User = User('user1', 'user1@email.com')
    user.save()
    profile: UserProfile = UserProfile(user)
    profile.save()

    article: Article = Article(user.profile, 'title', 'body', description='description')
    article.save()

    assert article.favourite(user.profile)
    assert article.is_favourite(user.profile)


def test_unlike_an_article_then_it_should_not_return_it(db_test) -> None:
    user1: User = User('user1', 'user1@email.com')
    user1.save()
    profile1: UserProfile = UserProfile(user1)
    profile1.save()
    user2: User = User('user2', 'user2@email.com')
    user2.save()
    profile2: UserProfile = UserProfile(user2)
    profile2.save()
    article: Article = Article(profile1, 'title', 'body', description='description')
    article.save()
    article.favourite(profile2)

    assert article.unfavourite(profile2)
    assert not article.is_favourite(profile2)


def test_when_a_tag_was_added_it_should_return_it(db_test, user: User):
    user = user.get()
    article: Article = Article(user.profile, 'title', 'body', description='description')
    article.save()

    tag1 = Tags(tag_name='tag1')
    tag2 = Tags(tag_name='tag2')

    assert article.add_tag(tag1)
    assert article.add_tag(tag2)
    assert len(article.tag_list) == 2


def test_remove_a_tag_was_added_it_should_return_remained(db_test, user: User):
    user = user.get()
    article: Article = Article(user.profile, 'title', 'body', description='description')
    article.save()

    tag1 = Tags(tag_name='tag1')
    tag2 = Tags(tag_name='tag2')
    article.add_tag(tag1)
    article.add_tag(tag2)

    assert article.remove_tag(tag1)
    assert article.remove_tag(tag2)
    assert len(article.tag_list) == 0


