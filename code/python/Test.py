y = [1] + [0] * 9
x = [1] * 10
def a():
    return [x for _ in range(10)],[y for _ in range(10)]
for t in a():
    print(len(t))