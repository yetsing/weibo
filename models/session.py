import time

from models import SQLModel
from utils import log


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
        result = self.expired_time < now
        log('expired', result, self.expired_time, now)
        return result
