from models import Model
from models.user import User
from models.weibo import Weibo
from models.comment import Comment
from models.session import Session


def test_data():
    Model.create_all()

    user_info = dict(
        username='name',
        password='123',
    )
    u, result = User.register(user_info)

    weibo = dict(
        content='I was born intelligent - education ruined me. --Bernard Shaw '
    )
    w = Weibo.add(weibo, u.id)

    comment = dict(
        content='good!',
        weibo_id=w.id,
    )
    Comment.add(comment, u.id)

    user_info = dict(
        username='uuuu',
        password='123',
    )
    u, result = User.register(user_info)

    Comment.add(comment, u.id)

    weibo = dict(
        content='For you，a thousand times over.',
    )
    Weibo.add(weibo, u.id)


if __name__ == '__main__':
    test_data()
