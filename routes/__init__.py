import time

from mou import (
    request,
    redirect,
    make_json,
)
from models.user import User
from models.session import Session


def current_user():
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        u = Session.get_user(session_id)
        return u
    else:
        return User.guest()


def login_required(route_function):
    def f():
        u = current_user()
        if u.is_guest():
            return redirect('/user/login/view')
        else:
            return route_function()

    return f


def ajax_login_required(route_function):
    def f():
        u = current_user()
        if u.is_guest():
            d = dict(
                status="fail",
                message="请登录",
            )
            return make_json(d)
        else:
            return route_function()

    return f


def owner_required(cls):
    def decorator(route_function):
        def f():
            u = current_user()
            if 'id' in request.query:
                m_id = request.query['id']
            else:
                m_id = request.json['id']
            m = cls.one_for_id(id=int(m_id))

            if m.user_id == u.id:
                return route_function()
            else:
                d = dict(
                    status="fail",
                    message="权限不足"
                )
                return make_json(d)

        return f

    return decorator


def formatted_time(t):
    time_format = '%Y-%m-%d'
    localtime = time.localtime(t)
    formatted = time.strftime(time_format, localtime)
    return formatted
