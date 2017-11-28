#--coding:utf-8--

foo = [2, 18, 9, 22, 17, 24, 8, 12, 27]

print(list(map(lambda x: x * 2 + 10 ,foo)))
print ([x for x in foo if x % 3 == 0])

data = []
data.append({"province":"beijing","order_price":100,"user_count":100,"total_price":10000})
data.append({"province":"shanghai","order_price":200,"user_count":50,"total_price":10000})
data.append({"province":"shenzhen","order_price":300,"user_count":100,"total_price":30000})
data.sort(key=lambda x:(x["user_count"],x["total_price"]),reverse=True)
for x in data:
    print(x)





li = [1,2,3]
li.extend(['a','b']) # 追加 iterator
print(li)
li.append('c') # 追加单个对象
print(li)
print(li.index(3),'----',li.index('a'))
li.insert(0,'开始位置insert')
print(li)
li.remove('a') # 移除首个出现的值
print(li)
li.reverse()
print(li,'反转')
li.remove('开始位置insert')
lili = li[:5]
print('lili---->',lili)
# lili.sort()  # 排序只能为 str 或 数字

print(lili)
