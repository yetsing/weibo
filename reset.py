import random

from models import Model
from models.user import User
from models.weibo import Weibo
from models.comment import Comment
from models.session import Session
from fake_data import *


def test_data():
    Model.create_all()

    for u in username:
        form = dict(
            username=u,
            password='123',
        )
        User.register(form)

    for w in weibos:
        form = dict(
            content=w,
        )
        Weibo.add(form, random.randint(0, 2))

    for c in comments:
        form = dict(
            content=c,
            weibo_id=random.randint(0, 4),
        )
        Comment.add(form, random.randint(0, 2))


if __name__ == '__main__':
    test_data()
