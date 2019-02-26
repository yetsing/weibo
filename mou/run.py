import _thread
import socket

from .requset import request
from .helper import *
from .static import static
from .route import route_dict, functions_before_request


def make_response(resp):
    if not isinstance(resp, Response):
        if isinstance(resp, str):
            resp = Response(resp)
        else:
            raise TypeError(
                'The view function did not return a valid response(string or bytes).'
            )
    return resp.content


def preprocess_request():
    for func in functions_before_request:
        r = func()
        if r is not None:
            return r


def response_from_request():
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    if request.path.startswith('/static'):
        return static(request)
    try:
        resp = preprocess_request()
        if resp is None:
            resp = route_dict[request.path]()
        return make_response(resp)
    except KeyError:
        return not_found()


def receive_request(connection):
    """
    接受请求
    """
    req = b''
    buffer_size = 521
    while True:
        r = connection.recv(buffer_size)
        req += r
        # 取到的数据长度不够 buffer_size 的时候，说明数据已经取完了。
        if len(r) < buffer_size:
            req = req.decode()
            return req


def process_request(connection):
    """
    接受请求并返回响应
    """
    with connection:
        r = receive_request(connection)
        # 浏览器会发空请求
        if len(r) > 0:
            request.set(r)
            log('{} {}'.format(request.method, request.path))
            response = response_from_request()
            connection.sendall(response)
        else:
            connection.sendall(b'')


def run(host, port):
    """
    启动服务器
    """
    log('Running on http://{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        s.listen()
        while True:
            connection, address = s.accept()
            _thread.start_new_thread(process_request, (connection,))
