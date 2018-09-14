from mou import register_route, run

from models import SQLModel

from routes.api_weibo import weibo
from routes.api_weibo_comment import comment
from routes.routes_public import default
from routes.routes_user import user


def configure():
    SQLModel.init_db()

    register_route(weibo, url_prefix='/weibo')
    register_route(comment, url_prefix='/comment')
    register_route(default)
    register_route(user)


if __name__ == '__main__':
    configure()

    config = dict(
        host='localhost',
        port=3000,
    )
    run(**config)
