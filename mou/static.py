import os


def safe_path(path: str):
    if '..' in path:
        raise FileNotFoundError("No such file or directory: '{}'".format(path))
    else:
        return path.replace('/', '\\')


def static(request):
    """
    静态资源的处理函数, 读取图片（或 JS 代码）并生成响应返回
    """
    parent = os.path.dirname(os.path.dirname(__file__))
    filename = safe_path(request.path)
    path = parent + filename
    if not os.path.isfile(path):
        raise FileNotFoundError("No such file or directory: '{}'".format(path))
    file_type = filename.rsplit('.', 1)[1]
    d = {
        'css': 'text/css',
        'js': 'application/javascript',
    }
    default = 'image/'.format(file_type)
    with open(path, 'rb') as f:
        header = 'HTTP/1.x 200 OK\r\ncontent-type: {}\r\n\r\n'.format(
            d.get(file_type, default)
        )
        r = header.encode() + f.read()
        return r
