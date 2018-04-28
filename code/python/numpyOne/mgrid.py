import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3
import scipy.stats as st

k,b=np.mgrid[1:3:8j,1:3:8j] # 1:3:3j分别代表1-3,4j是分割成四份
print(k.shape)
print(b.shape)
f_kb=3*k**2+2*b+1
# k.shape=1,-1  # 将3x3矩阵转为9x1列向量
# b.shape=1,-1
# f_kb.shape=1,-1 #统统转成9行1列

ax=plt.subplot(111,projection='3d')
ax.plot_surface(k,b,f_kb,rstride=1,cstride=1)
ax.set_xlabel('k')
ax.set_ylabel('b')
ax.set_zlabel('ErrorArray')
# p.show()

x, y = np.mgrid[-1:1:.01, -1:1:.01] # .01表示步长，啥情况，和上面不一样了
# print(x)
print((200,200)+(2,3) )  # (200, 200, 2, 3)
pos = np.empty(x.shape + (2,)) # 创建相应维度的随机矩阵
print('---->',np.empty(x.shape+(2,)).shape)
# print(pos)
pos[:, :, 0] = x
pos[:, :, 1] = y
rv = st.multivariate_normal([0, 0], [[1, 0], [0, 1]],(10,10)) # 第一个参数为平均值矩阵，第二个为协方差矩阵
print(rv)
plt.contourf(x, y, rv.pdf(pos))

plt.show()


x, y = np.random.multivariate_normal([0, 0], [[1, 0], [0, 1]], 10).T
plt.plot(x, y, 'x')
plt.axis('equal')
plt.show()



