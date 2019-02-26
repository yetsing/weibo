import datetime
import json
import time

from .response import Response


def not_found():
    """
    返回 404 响应
    """
    return b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>'


def format_expired_time(t):
    date = datetime.datetime.utcfromtimestamp(t)
    gmt_format = '%a, %d %b %Y %H:%M:%S GMT'
    ts = date.strftime(gmt_format)
    return ts


def redirect(url, status_code=302, headers=None, **kwargs):
    h = {
        'Location': url,
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)

    body = '''
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title>跳转中......</title>
        </head>
        <body>
            <p>如果页面没有自动跳转，请点击下面的链接手动跳转。</p>
            <a>{}</a>
        </body>
    </html>
    '''.format(url)

    response = Response(body, headers=headers)
    response.status_code = status_code
    return response


def make_json(data):
    """
    返回 json 格式的 body 数据
    """
    headers = {
        'Content-Type': 'application/json',
    }
    body = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(body, headers=headers)


def log(*args, **kwargs):
    time_format = '[%Y/%m/%d %H:%M:%S]'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    print(formatted, *args, **kwargs)
