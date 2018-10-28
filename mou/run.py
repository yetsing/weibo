import _thread
import socket

from .requset import Request
from .helper import *
from .static import static
from .mouse import route_dict

request = Request()


def finalize_request(content):
    if isinstance(content, bytes):
        return content
    else:
        r = make_response(content)
        return r.get_bytes()


def dispatch_request():
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    route_function = route_dict.get(request.path, error)
    if request.path.startswith('/static'):
        return static(request)
    b = route_function()
    return finalize_request(b)


def receive_request(connection):
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
        request.set(r)
        response = dispatch_request()
        # except:
        #     response = error(500)
        # 把响应发送给客户端
        connection.sendall(response)


def run(host, port):
    """
    启动服务器
    """
    with socket.socket() as s:
        s.bind((host, port))
        s.listen()
        while True:
            connection, address = s.accept()
            _thread.start_new_thread(process_request, (connection,))
