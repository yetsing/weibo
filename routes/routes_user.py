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

from models.user import User

user = Mou('user')


@user.route('/login')
def login():
    form = request.form
    u, result = User.login(form)

    session_id = str(uuid.uuid4())
    form = dict(
        session_id=session_id,
        user_id=u.id,
    )
    if not u.is_guest():
        Session.new(form)

    response = redirect('/login/view?result={}'.format(result))
    response.set_cookie('session_id', session_id)
    return response


@user.route('/login/view')
def login_view():
    u = current_user()
    result = request.query.get('result', '')
    result = unquote_plus(result)

    return render_template(
        'login.html',
        user=u,
        result=result,
    )


@user.route('/register')
def register():
    form = request.form
    u, result = User.register(form)
    return redirect('/login/view?result={}'.format(result))


@user.route('/register/view')
def register_view():
    u = current_user()
    result = request.query.get('result', '')
    result = unquote_plus(result)

    return render_template(
        'register.html',
        result=result,
        user=u,
    )
