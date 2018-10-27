import time

from models import SQLModel
from models.user import User


class Comment(SQLModel):
    sql_create = '''
        CREATE TABLE `Comment` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `content` Text NOT NULL,
        `user_id` INT NOT NULL REFERENCES User(id),
        `weibo_id` INT NOT NULL REFERENCES Weibo(id),
        `created_time` INT NOT NULL,
        `updated_time` INT NOT NULL,
        PRIMARY KEY (`id`)
    )'''

    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))
        self.created_time = form.get('created_time', -1)
        self.updated_time = form.get('updated_time', -1)

    def user(self):
        u = User.one_for_id(id=self.user_id)
        return u

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        form['created_time'] = int(time.time())
        form['updated_time'] = int(time.time())
        comment = cls.new(form)
        return comment
