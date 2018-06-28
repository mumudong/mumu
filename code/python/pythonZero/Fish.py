#--coding:utf-8--
class Fish:
    hungry = True
    print(hungry)
    def __init__(self):
        print('init')
    def eat(self,food):
        if food is not None:
            self.hungry = False
class User:
    age = None
    def __init__(self):
        self.name = 'name'
        self.age = 11
    def pt(self):
        print(self.name,self.age)
def impor():
    print('import test')
f = Fish()
u = User()
u.pt()
# Fish.eat(f,None)
# print(f.hungry)
# Fish.eat(f,"grass")
# f.eat("grass")
# print(f.hungry)
# u = User("张三")
# print(u.name)