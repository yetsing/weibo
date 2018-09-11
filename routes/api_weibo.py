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
        w = Weibo.find_by(id=int(weibo_id))

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
    u = User.find_by(id=user_id)
    data['username'] = u.username


# 给返回的 weibo 添加评论
def insert_comments(weibo):
    weibo_id = weibo['id']
    comments = Comment.find_all(weibo_id=weibo_id)
    comments = [c.json() for c in comments]
    # 添加评论的用户名
    for i, c in enumerate(comments):
        insert_username(c)

    weibo['comments'] = comments


@weibo.route('/index')
def index():
    """
    weibo 首页的路由函数
    """
    u = current_user()
    weibos = Weibo.find_all(user_id=u.id)
    # 替换模板文件中的标记字符串
    return render_template('weibo_index.html', weibos=weibos, user=u)


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
@weibo.route('/all')
def all():
    weibos = Weibo.all_json()
    for i, w in enumerate(weibos):
        # 添加用户名和评论
        insert_username(w)
        insert_comments(w)
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
    # 删除 weibo 对应的 comment
    comments = Comment.find_all(weibo_id=weibo_id)
    for c in comments:
        Comment.delete(c.id)

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
    form = request.json
    log('api weibo update form', form)
    t = Weibo.update(**form)
    return make_json(t.json())
