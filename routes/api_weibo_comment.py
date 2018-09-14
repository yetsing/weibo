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
from models.user import User

comment = Mou('comment')


def comment_owner_required(route_function):
    def f():
        log('same_user_required')
        u = current_user()
        if 'id' in request.query:
            comment_id = request.query['id']
        else:
            comment_id = request.json['id']
        c = Comment.one(id=int(comment_id))

        if c.user_id == u.id:
            return route_function()
        else:
            d = dict(
                done="false",
                message="权限不足"
            )
            return make_json(d)

    return f


# 添加用户名
def insert_username(data):
    user_id = data.pop('user_id')
    u = User.one(id=user_id)
    data['username'] = u.username


@comment.route('/all')
def all():
    u = current_user()
    weibo_id = int(request.query.get('weibo_id'))
    comments = Comment.all(weibo_id=weibo_id)
    data = [c.json() for c in comments]
    for d in data:
        # 添加用户名
        insert_username(d)
    ud = {'username': u.username}
    data.append(ud)
    return make_json(data)


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
    form = request.json
    t = Comment.update(**form)
    return make_json(t.json())
