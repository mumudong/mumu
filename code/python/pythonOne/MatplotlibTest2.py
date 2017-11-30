#--coding:utf-8--
import numpy as npy
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体,否则会乱码
plt.rcParams['axes.unicode_minus'] = False
plt.xlabel('x轴')
plt.ylabel('y轴')
plt.title('title')
plt.ylim(0,10) #设置y轴范围
plt.xlim(0,6)
plt.annotate('这是注释',xy=(2,5),xytext=(3,5),
             arrowprops=dict(facecolor='red',shrink=0.05)) #xy是箭头头部，xytext是尾部
plt.text(1,7,'text示例',horizontalalignment='center',fontsize=10,verticalalignment='center') #前两位是显示示例的x,y坐标
plt.legend() #设置图示


plt.plot([1,2,3], [1,5,3], 'go-', label='line 1', linewidth=2)
plt.show()