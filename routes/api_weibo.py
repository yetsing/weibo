from mou import (
    Mou,
    log,
    request,
    make_json,
    render_template,
)

from routes import (
    current_user,
    ajax_login_required,
)
from models.comment import Comment
from models.weibo import Weibo
from models.user import User

weibo = Mou('weibo')


def weibo_owner_required(route_function):
    def f():
        log('same_user_required')
        u = current_user()
        if 'id' in request.query:
            weibo_id = request.query['id']
        else:
            weibo_id = request.json['id']
        w = Weibo.one_for_id(id=int(weibo_id))

        if w.user_id == u.id:
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
    u = User.one_for_id(id=user_id)
    data['username'] = u.username


@weibo.route('/index')
def index():
    """
    weibo 首页的路由函数
    """
    u = current_user()
    return render_template('weibo-index.html', user=u)


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
@weibo.route('/all')
def all():
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
    # 创建一个 weibo
    u = current_user()
    t = Weibo.add(form, u.id)
    # 添加用户名和评论
    data = t.json()
    data['username'] = u.username
    data['comments'] = []
    return make_json(data)


@weibo.route('/delete')
@ajax_login_required
@weibo_owner_required
def delete():
    weibo_id = int(request.query['id'])
    Weibo.delete(weibo_id)

    d = dict(
        message="成功删除 weibo"
    )
    return make_json(d)


@weibo.route('/update')
@ajax_login_required
@weibo_owner_required
def update():
    """
    用于增加新 weibo 的路由函数
    """
    u = current_user()
    form = request.json
    form['user_id'] = u.id
    log('api weibo update form', form)
    t = Weibo.update(**form)
    return make_json(t.json())
