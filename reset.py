import random
import pymysql

import secret
import config
from fake_data import *
from models import SQLModel
from models.session import Session
from models.weibo import Weibo
from models.user import User
from models.comment import Comment


def recreate_table(cursor):
    cursor.execute(User.sql_create)
    cursor.execute(Session.sql_create)
    cursor.execute(Weibo.sql_create)
    cursor.execute(Comment.sql_create)


def recreate_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=secret.mysql_password,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        cursor.execute(
            'DROP DATABASE IF EXISTS `{}`'.format(
                config.db_name
            )
        )
        cursor.execute(
            'CREATE DATABASE `{}` DEFAULT CHARACTER SET utf8mb4'.format(
                config.db_name
            )
        )
        cursor.execute('USE `{}`'.format(config.db_name))

        recreate_table(cursor)

    connection.commit()
    connection.close()


def insert_test_data():
    SQLModel.init_db()

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
        Weibo.add(form, random.randint(1, 3))

    for c in comments:
        form = dict(
            content=c,
            weibo_id=random.randint(1, 5),
        )
        Comment.add(form, random.randint(1, 3))


if __name__ == '__main__':
    recreate_database()
    insert_test_data()
