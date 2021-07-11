from flask_realworld.articles.models.comment import Comment


def test_when_make_a_comment_then_it_should_return_it(db_test, user, article) -> None:
    user = user.get()
    comment: Comment = Comment(article, user.profile, 'comment body')
    comment.save()

    assert comment.article == article
    assert comment.author == user.profile
    assert article.comments.count() == 1


def test_when_delete_a_comment_then_it_should_not_return_it(db_test, user, article) -> None:
    user = user.get()
    comment: Comment = Comment(article, user.profile, 'comment body')
    comment.save()

    comment.delete()
    assert article.comments.count() == 0

