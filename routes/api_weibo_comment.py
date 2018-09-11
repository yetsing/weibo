from mou import (
    Mou,
    log,
    request,
    make_json,
)

from routes import (
    ajax_login_required,
    current_user
)
from models.comment import Comment

comment = Mou('comment')


def comment_owner_required(route_function):
    def f():
        log('same_user_required')
        u = current_user()
        if 'id' in request.query:
            comment_id = request.query['id']
        else:
            comment_id = request.json['id']
        c = Comment.find_by(id=int(comment_id))

        if c.user_id == u.id:
            return route_function()
        else:
            d = dict(
                done="false",
                message="权限不足"
            )
            return make_json(d)

    return f


@comment.route('/add')
@ajax_login_required
def add():
    form = request.json
    # 创建一个 comment
    u = current_user()
    c = Comment.add(form, u.id)
    # 添加用户名
    data = c.json()
    data['username'] = u.username
    return make_json(data)


@comment.route('/delete')
@ajax_login_required
@comment_owner_required
def delete():
    comment_id = int(request.query['id'])
    Comment.delete(comment_id)
    d = dict(
        message="成功删除 comment"
    )
    return make_json(d)


@comment.route('/update')
@ajax_login_required
@comment_owner_required
def update():
    """
    用于增加新 weibo 的路由函数
    """
    form = request.json
    log('api weibo update form', form)
    t = Comment.update(**form)
    return make_json(t.json())
