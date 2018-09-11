import uuid
from urllib.parse import unquote_plus
from mou import (
    Mou,
    request,
    redirect,
    make_response,
    render_template,
)

from models.session import Session
from routes import current_user

from mou import log
from models.user import User

user = Mou('user')


@user.route('/login')
def login():
    """
    登录页面的路由函数
    """
    form = request.form

    u, result = User.login(form)

    session_id = str(uuid.uuid4())
    form = dict(
        session_id=session_id,
        user_id=u.id,
    )
    Session.new(form)

    r = redirect('/user/login/view?result={}'.format(result))
    response = make_response(r)
    response.set_cookie('session_id', session_id)
    return response


@user.route('/login/view')
def login_view():
    u = current_user()
    result = request.query.get('result', '')
    result = unquote_plus(result)

    return render_template(
        'login.html',
        username=u.username,
        result=result,
    )


@user.route('/register')
def register():
    """
    注册页面的路由函数
    """
    form = request.form

    u, result = User.register(form)
    log('register post', result)

    return redirect('/user/register/view?result={}'.format(result))


@user.route('/register/view')
def register_view():
    result = request.query.get('result', '')
    result = unquote_plus(result)

    return render_template('register.html', result=result)
