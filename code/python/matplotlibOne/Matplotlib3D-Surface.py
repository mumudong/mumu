#--coding:utf-8--

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as stats
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.io as sio

def d1():
    fig = plt.figure('3D-surface')
    # ax = Axes3D(fig)
    ax = fig.add_subplot(111, projection='3d')
    # 初始化角度，否是z轴是反的
    ax.view_init(30,35)

    X = np.arange(-4,4,0.25)
    Y = np.arange(-4,4,0.25)
    X,Y = np.meshgrid(X,Y)
    # print('x---->\n',X,'\ny---->\n',Y)
    R = np.sqrt( X ** 2 + Y ** 2)
    Z = np.sin(R)
    # ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap='rainbow')
    ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap=plt.cm.hot)
    ax.contourf(X, Y, Z, zdir='z', offset=-2, cmap=plt.cm.hot)
    ax.set_zlim(-2,2)
    plt.show()

'''
绘制2维高斯分布
'''
def d2():
    fig = plt.figure()
    ax = Axes3D(fig)
    rv = stats.multivariate_normal([0, 0], cov=1)
    x, y = np.mgrid[-3:3:.15, -3:3:.15]
    ax.plot_surface(x, y, rv.pdf(np.dstack((x, y))), rstride=1, cstride=1)
    ax.set_zlim(0, 0.2)
    # savefig('../figures/plot3d_ex.png',dpi=48)
    plt.show()

'''
绘制正方体和四面体示例
'''
def d3():
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # 正文体顶点和面
    verts = [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1), (1, 0, 1)]
    faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [0, 3, 7, 4]]
    # 四面体顶点和面
    # verts = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 0, 1)]
    # faces = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
    # 获得每个面的顶点
    poly3d = [[verts[vert_id] for vert_id in face] for face in faces]
    # print(poly3d)

    # 绘制顶点
    x, y, z = zip(*verts)
    ax.scatter(x, y, z)
    # 绘制多边形面
    ax.add_collection3d(Poly3DCollection(poly3d, facecolors='b', linewidths=1, alpha=0.02))
    # ax.add_collection3d(Line3DCollection(poly3d, colors='k', linewidths=0.5, linestyles=':'))

    # 设置图形坐标范围
    ax.set_xlabel('X')
    ax.set_xlim3d(-0.5, 1.5)
    ax.set_ylabel('Y')
    ax.set_ylim3d(-0.5, 1.5)
    ax.set_zlabel('Z')
    ax.set_zlim3d(-0.5, 1.5)
    plt.show()

def d4():
    mat1 = '../file/4a.mat' #这是存放数据点的文件，需要它才可以画出来
    data = sio.loadmat(mat1)
    m = data['data']

    x,y,z = m[0],m[1],m[2]
    ax=plt.subplot(111,projection='3d') #创建一个三维的绘图工程

    #将数据点分成三部分画，在颜色上有区分度
    # ax.scatter(x[:1000],y[:1000],z[:1000],c='y')          #绘制数据点
    # ax.scatter(x[1000:4000],y[1000:4000],z[1000:4000],c='r')
    ax.scatter(x[4000:],y[4000:],z[4000:],c='g')

    ax.set_zlabel('Z') #坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()


if __name__ == '__main__':
    # d1()
    # d2()
    # d3()
    d4()
    print('ok')