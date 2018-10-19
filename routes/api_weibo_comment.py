from mou import (
    Mou,
    request,
    make_json,
)

from routes import (
    current_user,
    owner_required,
    ajax_login_required,
)

from models.comment import Comment
from models.user import User
from utils import log

comment = Mou('comment')


# 添加用户名
def insert_username(data):
    user_id = data.pop('user_id')
    u = User.one(id=user_id)
    data['username'] = u.username


@comment.route('/all')
def all():
    u = current_user()
    weibo_id = int(request.query.get('weibo_id'))
    comments = Comment.all(weibo_id=weibo_id, sort_by='created_time')
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
@owner_required(Comment)
def delete():
    comment_id = int(request.query['id'])
    Comment.delete(comment_id)
    d = dict(
        message="成功删除 comment"
    )
    return make_json(d)


@comment.route('/update')
@ajax_login_required
@owner_required(Comment)
def update():
    form = request.json
    t = Comment.update(**form)
    return make_json(t.json())
