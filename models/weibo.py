import time

from models import SQLModel
from models.comment import Comment


class Weibo(SQLModel):
    sql_create = '''
    CREATE TABLE `Weibo` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `content` Text NOT NULL,
        `user_id` INT NOT NULL,
        `created_time` INT NOT NULL,
        `updated_time` INT NOT NULL,
        `comment_count` INT NULL,
        PRIMARY KEY (`id`)
    )'''

    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', None)
        self.created_time = form.get('created_time', -1)
        self.updated_time = form.get('updated_time', -1)
        self.comment_count = Comment.count(weibo_id=self.id)

    def comments(self):
        cs = Comment.all(weibo_id=self.id)
        return cs

    @staticmethod
    def all_json():
        weibos = Weibo.all(desc=False)
        ws = [w.__dict__ for w in weibos]
        return ws

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        form['created_time'] = int(time.time())
        form['updated_time'] = int(time.time())
        weibo = cls.new(form)
        return weibo

    @classmethod
    def delete(cls, weibo_id):
        # 删除 weibo 对应的 comment
        comments = Comment.all(weibo_id=weibo_id)
        for c in comments:
            Comment.delete(c.id)
        super().delete(weibo_id)

    @classmethod
    def update(cls, id, **kwargs):
        kwargs['updated_time'] = int(time.time())
        super().update(id, **kwargs)
        w = cls(kwargs)
        return w
