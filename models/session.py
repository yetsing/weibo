import time

from models import SQLModel
from models.user import User


class Session(SQLModel):
    sql_create = '''
    CREATE TABLE `Session` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `session_id` CHAR(36) NOT NULL,
        `user_id` INT NOT NULL,
        `expired_time` INT NOT NULL,
        PRIMARY KEY (`id`)
    )'''

    def __init__(self, form):
        super().__init__(form)
        self.session_id = form.get('session_id', '')
        self.user_id = form.get('user_id', -1)
        self.expired_time = form.get('expired_time', time.time() + 3600)

    def expired(self):
        now = time.time()
        expired = self.expired_time < now
        if expired:
            Session.delete(self.id)
        return expired

    @classmethod
    def get_user(cls, session_id):
        s = cls.one(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.one_for_id(id=user_id)
            return u
