#--coding:utf-8--
import matplotlib.pyplot as plt

labels = []
quants = []

for line in open('../file/major_country_gdp').readlines():
    info = line.split()
    labels.append(info[0])
    quants.append(info[1])

plt.figure(2,(6,6))
# For China, make the piece explode a bit
def explode(label,target='China'):
    if label == target:return 0.1
    else:return 0

'''
map()是 Python 内置的高阶函数，它接收一个函数 f 和一个 list，
并通过把函数 f 依次作用在 list 的每个元素上，得到一个新的 list 并返回
'''
expl = list(map(explode,labels))
print(expl.__len__(),
      '\n',
      quants)
colors = ['pink','coral','yellow','orange']

plt.pie(quants,explode=list(expl),colors=colors,labels=labels,
        autopct='%1.1f%%',pctdistance=0.8,shadow=True)
plt.title('top 10 GDP countries',bbox={'facecolor':'0.8','pad':5})

plt.show()



