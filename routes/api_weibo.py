from mou import (
    Mou,
    request,
    make_json,
    render_template,
)

from routes import (
    current_user,
    owner_required,
    ajax_login_required,
)

from models.weibo import Weibo
from models.user import User

weibo = Mou('weibo')


# 添加用户名
def insert_username(data):
    user_id = data.pop('user_id')
    u = User.one_for_id(id=user_id)
    data['username'] = u.username


@weibo.route('/index')
def index():
    u = current_user()
    return render_template('weibo-index.html', user=u)


@weibo.route('/all')
def get_all():
    u = current_user()
    weibos = Weibo.all_json()
    for i, w in enumerate(weibos):
        # 添加用户名
        insert_username(w)
    d = {'username': u.username}
    weibos.append(d)
    return make_json(weibos)


@weibo.route('/add')
@ajax_login_required
def add():
    form = request.json
    u = current_user()
    t = Weibo.add(form, u.id)
    data = t.json()
    # 添加用户名和评论
    data['username'] = u.username
    data['comments'] = []
    return make_json(data)


@weibo.route('/delete')
@owner_required(Weibo)
def delete():
    weibo_id = int(request.query['id'])
    Weibo.delete(weibo_id)

    d = dict(
        message="成功删除 weibo"
    )
    return make_json(d)


@weibo.route('/update')
@owner_required(Weibo)
def update():
    u = current_user()
    form = request.json
    form['user_id'] = u.id
    t = Weibo.update(**form)
    return make_json(t.json())
