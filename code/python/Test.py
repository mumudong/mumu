y = [1] + [0] * 9
x = [1] * 10
def a(): # 返回 Tuple
    return [x for _ in range(10)],[y for _ in range(10)]
for t in a():
    print(t)
for (x,y) in zip(range(4),range(4)):
    print(x,y)