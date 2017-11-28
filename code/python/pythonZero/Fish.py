#--coding:utf-8--
class Fish:
    hungry = True
    def eat(self,food):
        if food is not None:
            self.hungry = False
class User:
    def __init__(self,name):
        self.name = name
f = Fish()
Fish.eat(f,None)
print(f.hungry)
Fish.eat(f,"grass")
f.eat("grass")
print(f.hungry)
u = User("张三")
print(u.name)