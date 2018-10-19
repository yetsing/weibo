import time

from mou import (
    request,
    redirect,
    make_json,
)
from models.user import User
from models.session import Session
from utils import log


def current_user():
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        s = Session.one(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.one_for_id(id=user_id)
            return u
    else:
        return User.guest()


def login_required(route_function):
    def f():
        log('login_required')
        u = current_user()
        if u.is_guest():
            log('游客用户')
            return redirect('/user/login/view')
        else:
            log('登录用户', route_function)
            return route_function()

    return f


def ajax_login_required(route_function):
    def f():
        log('ajax_login_required')
        u = current_user()
        if u.is_guest():
            d = dict(
                status="fail",
                message="请登录",
            )
            return make_json(d)
        else:
            log('登录用户', u.username)
            return route_function()

    return f


def owner_required(cls):
    def decorator(route_function):
        def f():
            log('same_user_required')
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
