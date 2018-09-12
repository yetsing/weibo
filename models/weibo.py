from models import Model
from models.comment import Comment


class Weibo(Model):
    """
    微博类
    """

    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', None)
        self.created_time = form.get('created_time', -1)
        self.updated_time = form.get('updated_time', -1)
        self.comment_count = form.get('comment_count', 0)

    def comments(self):
        cs = Comment.find_all(weibo_id=self.id)
        return cs
