import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
# 泊松分布,泊松分布的期望和方差均为 lamda
# 概率函数 P(X=K) = (lameda ** k) * (e ** -lamda)/ k!
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
y = st.multivariate_normal.pdf(x, mean=2.5, cov=.5)
plt.plot(x,y)
plt.show()

x, y = np.mgrid[-1:1:.01, -1:1:.01]
pos = np.empty(x.shape + (2,))
pos[:, :, 0] = x; pos[:, :, 1] = y
rv = st.multivariate_normal([0, 0], [[1, 0], [0, 1]])
plt.contourf(x, y, rv.pdf(pos))
plt.show()



