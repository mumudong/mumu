import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
# 泊松分布,泊松分布的期望和方差均为 lamda
# 概率函数 P(X=K) = (lameda ** k) * (e ** -lamda)/ k!
# n次投硬币，正面朝上的概率为p, np为定值
# 二项分布 n趋向无穷大，p趋向无穷小时推出泊松分布.
'''
rvs：对随机变量进行随机取值，可以通过size参数指定输出的数组的大小。
pdf：随机变量的概率密度函数。
cdf：随机变量的累积分布函数，它是概率密度函数的积分。
sf：随机变量的生存函数，它的值是1-cdf(t)。
ppf：累积分布函数的反函数。
stat：计算随机变量的期望值和方差。
fit：对一组随机取样进行拟合，找出最适合取样数据的概率密度函数的系数。
'''
F_true = 1000
N = 50
F = st.poisson(F_true).rvs(N) # rvs采样50个
print(F)

# mu_true, sigma_true = 1000, 15
# N = 100
# F_true = st.norm(mu_true, sigma_true).rvs(N)
# F = st.poisson(F_true).rvs()
# print(F)

# 二项分布
n,p = 100,.5
X = st.binom(n,p)
print(X.mean(),X.std())
'''
pdf 表示的是函数，给一定输入值，就会得到一个输出值，而不是随机变量。
st.norm.pdf(0, loc=0, scale=1) ⇒ 1/sqrt((2pi)**0.5)
如下代码绘制出  1/((2pi)**0.5) * e ** (- (x-1)**2/2)
'''
mu, sigma = 1, 1
xs = np.linspace(-5, 5, 1000)
plt.plot(xs, st.norm.pdf(xs, loc=mu, scale=sigma))
plt.show()

# st.multivariate_normal：多元正态分布；
x = np.linspace(0, 5, 10, endpoint=False)
y = st.multivariate_normal.pdf(x, mean=4, cov=.5)
plt.plot(x,y)
plt.show()

x, y = np.mgrid[-1:1:.5, -1:1:.5]
pos = np.empty(x.shape + (2,))
pos[:, :, 0] = x; pos[:, :, 1] = y
print(x)
print(y)
'''
多元正态分布
参数1：均值向量，即每一个特征的均值组成的向量
参数2：分布的协方差矩阵
'''
rv = st.multivariate_normal([0, 0], [[1, 0], [0, 1]]) # 协方差随机分布
print(rv.pdf(pos))
print(rv.pdf(pos).sum())
print(type(rv))
print(rv.dim)
# x,y均为2维
plt.contourf(x, y, rv.pdf(pos)) # pdf接受的参数是三维数据，第三维代表一个数据坐标，1、2维代表网格坐标位置。
plt.show()



