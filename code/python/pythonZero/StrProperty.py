#--coding:utf-8--
'''
 查看帮助
 help("keywords")
 查看import关键字如何使用
 help("import")
 查看模块的使用
 help("os.path")
 查看list如何使用
 help("list")
 查看字符串中find方法使用
 help("str.find")
 查看内置函数如何使用
 help("open")
'''
help("str.find")
'''
# \符号可以换行
weather_is_hot = None
today_is_wednesday = None
if(weather_is_hot != 1) and \
    (today_is_wednesday != 1):
    print 'today is wednesday and weather is hot!'
'''

# 不等于号的表示
# print 1!=2
# print 1<>2

# 与、或、非逻辑符
# print True and False
# print True or False
# print not not None




# 三引号的功能
'''Looking for work or have a Python related position 
    that you're trying to hire for? 
    Our community-run job board is the place to go.'''



a = 'a1bb'
print(type(a)) #类型
b = a.capitalize()  #小写转大写
print(a,"--capitalize小写转大写-->",b)
a = b.casefold() # 大写转小写
print(b,"--casefold大写转小写-->",a)

print(a.center(20),'字符串居中，使用空格填充长度为width的空字符串')
print(a.count('b'),'返回sub在字符串里边出现的次数')
print(a.find('c'),'检测sub是否包含于字符串，找不到返回-1，否则返回0')
print(a.isalnum(),'字符串至少有一个字符并且都是字母或数字返回true')
print(a.isalpha(),'字符串中至少有一个字符且全为字母返回true')
print(a.isdecimal(),'字符串至少一个字符且为十进制返回true')

print(a.join('----')) #- a1bb-a1bb-a1bb-













