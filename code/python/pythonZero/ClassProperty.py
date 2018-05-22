#--coding:utf-8--
#内置属性:
#    __dict__:用来存储属性的字典,使用点来访问属性本质.字典会占用大量内存,
# x = 在需要管理一些资源比如文件
# __slots__是什么:是一个类变量,变量值可以是列表,元祖,或者可迭代对象,也可以是一个字符串(意味着所有实例只有一个数据属性
'''
类的方法
在类地内部，使用 def 关键字来定义一个方法，与一般函数定义不同，类方法必须包含参数 self, 且为第一个参数，self 代表的是类的实例。
self 的名字并不是规定死的，也可以使用 this，但是最好还是按照约定是用 self

__private_attrs：两个下划线开头，这种用法是为了避免与子类定义的名称冲突,类似final

_单下划线私有方法 

class people:  
    name="tom"      #类属性:实例对象和类对象可以同时调用  
    def  __init__(self,age):    #实例属性  
        self.age=age 

class people:  
    name="tom"      #类属性:实例对象和类对象可以同时调用  
    def  __init__(self,age):    #实例属性  
        self.age=age  
  
p=people(18)    #实例对象  
p.sex="男"       #实例属性  
print(p.name)  
print(p.age)    #实例属性是实例对象特有的，类对象不能拥有  
print(p.sex)  
print(people.name)  #类对象  
# print(people.age)  #错误：实例属性，不能通过类对象调用  
# print(people.sex)  #错误：实例属性，不能通过类对象调用


类方法
class people:  
    country="china"  
    @classmethod  
    def getCountry(cls):  
        return cls.country  
p=people()  
print(p.getCountry())   #实例对象调用类方法  
print(people.getCountry())  #类对象调用类方法  










'''


#内置方法:
#__new__:在初始化一个类对象时，基本的逻辑是，先通过__new__实例化一个对象，然后return，而__init__方法接收的第一个参数self，
#        就是new返回的此类实例化的对象


#    __init__ :构造方法，如 obj = Single() 会触发该方法
#    __call__ :构造对象后，对象加括号触发,如 obj(),或 Single()()
#    __setattr__:增加、修改属性会触发该方法，若重写并在该方法下使用 self.key=value会无限递归，若重写，赢self.__dict__[key]=value
#    __delattr__:若重写该方法，并在该方法下使用 del self.item会造成无限递归，应为 self.__dict__.pop(item)
#    __getattr__:只有在使用点调用属性且属性不存在的时候才会触发
#    __getattribute__:不管属性存在与否，都会调用
#    __getitem__: obj['name'] 触发
#    __setitem__: obj['name']='小明' 触发
#    __delitem__: del obj['name'] 触发
#    __delattr__: del obj.name 触发
#    __str__: print(obj) 等价于调用 obj.__str__(),__repr__和__str__实现的功能是一样的，如果两个共存，只会调用__str__，在没有定义__str__的情况下调用__repr__。
#    __del__:称作析构方法,当对象在内存中被释放时，自动触发执行。
#    __iter__, __next__实现迭代器协议
#    class Foo:
#        def __init__(self,start,stop):
#            self.num=start
#            self.stop=stop
#        def __iter__(self):
#            return self
#        def __next__(self):
#            if self.num >= self.stop:
#                raise StopIteration
#            n=self.num
#            self.num+=1
#            return n
#    for i in Foo(1,5):
#        print(i)


#    with语句的应用：
#    使用with语句的目的就是把代码块放入with中执行，with结束后，自动完成清理工作，无须手动干预
#    ，网络连接和锁的编程环境中，可以在__exit__中定制自动释放资源的机制，无须再去关心这个问题。


#   class Open(object):
#       def __init__(self, name):
#           self.name = name
#
#       def __enter__(self):
#           print('run __enter__')
#           return self
#
#       def __exit__(self, exc_type, exc_val, exc_tb):
#           print('run __exit__')
#           print('exc_type: [%s]' % exc_type)
#           print('exc_val: [%s]' % exc_val)
#           print('exc_tb: [%s]' % exc_tb)
#           return True

# with Open('a.txt') as f:
#     print('test start...')
#     print(f.name)
#     print(dfsdfasdfasdasfsa)
#     print('anything else')
#
# print('---end---')

# >>
# run __enter__
# test start...
# a.txt
# run __exit__
# exc_type: [<class 'NameError'>] # 异常类型
# exc_val: [name 'dfsdfasdfasdasfsa' is not defined] # 异常内容
# exc_tb: [<traceback object at 0x00000170FAD639C8>] # traceback
# ---end---

# class A(object):
#     bar = 1
#     def foo(self):
#         print 'foo'

    # @staticmethod
    # def static_foo():
    #     print 'static_foo'
    #     print A.bar

    # @classmethod
    # def class_foo(cls):
    #     print 'class_foo'
    #     print cls.bar
    #     cls().foo()

# A.static_foo()
# A.class_foo()











