#--coding:utf-8--
class Single(object):
    _instance = None
    def __new__(cls, *args, **kwargs):# *表示可变参数 **表示字典类可变参数
        if not cls._instance:
            cls._instance = super(Single,cls).__new__(cls,*args,**kwargs)