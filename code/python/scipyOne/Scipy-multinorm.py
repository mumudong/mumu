import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import matplotlib as mpl

num = 200
l = np.linspace(-5,5,num)
X, Y =np.meshgrid(l, l) # 产生三维曲面的分割点坐标

u = np.array([0, 0])
o = np.array([[1, 0.5],
              [0.5, 1]])
print(u)
print(o)
u = np.array([1, 1])
o = np.array([[1, 0],
              [0, 1]])
u = np.array([1, 1])
o = 3*np.array([[1, 0],
                [0, 1]])

pos = np.concatenate((np.expand_dims(X,axis=2),np.expand_dims(Y,axis=2)),axis=2)
print('X---->\n',X)
print('expend---->\n',np.expand_dims(X,axis=2))
print(X.shape,np.expand_dims(X,axis=2).shape,pos.shape)

a = (pos-u).dot(np.linalg.inv(o))
b = np.expand_dims(pos-u,axis=3)
Z = np.zeros((num,num), dtype=np.float32)
for i in range(num):
    Z[i] = [np.dot(a[i,j],b[i,j]) for j in range(num)]
Z = np.exp(Z*(-0.5))/(2*np.pi*np.linalg.det(o))
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.plot_surface(X, Y, Z, rstride=5, cstride=5, alpha=0.7, cmap=cm.coolwarm)

cset = ax.contour(X,Y,Z,10,zdir='z',offset=0,cmap=cm.coolwarm)
cset = ax.contour(X, Y, Z, zdir='x', offset=-5,cmap=mpl.cm.winter)
cset = ax.contour(X, Y, Z, zdir='y', offset= 5,cmap= mpl.cm.winter)
'''
mpl.cm.rainbow
mpl.cm.winter
mpl.cm.bwr  # 蓝，白，红
cm.coolwarm
'''

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()