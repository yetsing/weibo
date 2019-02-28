from mou import (
    Mou,
    request,
    make_json,
)
from .helper import (
    insert_username,
    owner_required,
    ajax_login_required,
)
from models.comment import Comment

comment = Mou('comment')


@comment.route('/all')
def get_all():
    u = request.current_user
    weibo_id = int(request.query.get('weibo_id'))
    comments = Comment.all(weibo_id=weibo_id, sort_by='created_time')
    data = [c.json() for c in comments]
    for d in data:
        insert_username(d)
    ud = {'username': u.username}
    data.append(ud)
    return make_json(data)


@comment.route('/add')
@ajax_login_required
def add():
    form = request.json
    u = request.current_user
    c = Comment.add(form, u.id)
    data = c.json()
    data['username'] = u.username
    return make_json(data)


@comment.route('/delete')
@owner_required(Comment)
def delete():
    comment_id = int(request.query['id'])
    Comment.delete(comment_id)
    d = dict(
        message="成功删除 comment"
    )
    return make_json(d)


@comment.route('/update')
@owner_required(Comment)
def update():
    form = request.json
    t = Comment.update(**form)
    return make_json(t.json())
