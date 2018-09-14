import json
import os
import time

from models.user_role import (
    QinEncoder,
    qin_decode,
)

from mou import log


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False, cls=QinEncoder)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s, object_hook=qin_decode)


def formatted_time(t):
    time_format = '%Y-%m-%d'
    localtime = time.localtime(t)
    formatted = time.strftime(time_format, localtime)
    return formatted


class Model(object):
    """
    Model 是所有 model 的基类
    """

    def __init__(self, form):
        self.id = form.get('id', None)
        # self.id = None

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m

    @classmethod
    def add(cls, form, user_id):
        m = cls(form)
        m.user_id = user_id
        m.created_time = int(time.time())
        m.updated_time = formatted_time(m.created_time)
        m.save()

        return m

    @classmethod
    def delete(cls, id):
        ms = cls.all()
        for i, m in enumerate(ms):
            if m.id == id:
                del ms[i]
                break
        ns = [m.__dict__ for m in ms]
        path = cls.db_path()
        save(ns, path)

    @classmethod
    def update(cls, **kwargs):
        id = int(kwargs['id'])
        m = cls.find_by(id=id)
        kwargs.pop('id')

        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)

        m.updated_time = formatted_time(int(time.time()))

        m.save()
        return m

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        ms = [cls(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        log('find_by kwargs', kwargs)

        for m in cls.all():
            exist = True
            for k, v in kwargs.items():
                if not hasattr(m, k) or not getattr(m, k) == v:
                    exist = False
            if exist:
                return m

    @classmethod
    def find_all(cls, **kwargs):
        log('find_all kwargs', kwargs)
        models = []

        for m in cls.all():
            print('every comment', m)
            exist = True
            for k, v in kwargs.items():
                if not hasattr(m, k) or not getattr(m, k) == v:
                    exist = False
            if exist:
                models.append(m)

        return models

    def save(self):
        models = self.all()
        log('models', models)

        if self.id is None:
            # 添加 id
            if len(models) > 0:
                log('不是第一个元素', models[-1].id)
                self.id = models[-1].id + 1
            else:
                log('第一个元素')
                self.id = 0
            models.append(self)
        else:
            # 更新数据
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        ns = [m.__dict__ for m in models]
        path = self.db_path()
        save(ns, path)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)

    def json(self):
        d = self.__dict__
        return d

    @classmethod
    def all_json(cls):
        ms = cls.all()
        js = [t.json() for t in ms]
        return js

    @classmethod
    def create_all(cls):
        if not os.path.exists('data'):
            os.mkdir('data')
        subclasses = cls.__subclasses__()
        for c in subclasses:
            f = open(c.db_path(), 'w')
            f.write('[]')
            f.close()
