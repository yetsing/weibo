from mou import render_template, Mou
from routes import current_user

default = Mou('index')


@default.route('/')
def index():
    """
    主页的处理函数, 返回主页的响应
    """
    u = current_user()
    return render_template('index.html', username=u.username)
