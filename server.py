from mou import register_mou, run

from models import SQLModel

from routes.api_weibo import weibo
from routes.api_weibo_comment import comment
from routes.routes_public import default
from routes.routes_user import user


def main():
    SQLModel.init_db()

    register_mou(default)
    register_mou(user)
    register_mou(weibo, url_prefix='/weibo')
    register_mou(comment, url_prefix='/comment')

    config = dict(
        host='localhost',
        port=3000,
    )
    run(**config)


if __name__ == '__main__':
    main()

