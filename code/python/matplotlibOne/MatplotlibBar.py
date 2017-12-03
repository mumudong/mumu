#--coding:utf-8--

import matplotlib.pyplot as plt
import numpy as np

labels = []
quants = []

for line in open('../file/major_country_gdp').readlines():
    info = line.split()
    labels.append(info[0])
    quants.append(int(info[1]))
print('x-->',labels,'\ny-->',quants)
width = 0.4
ind = np.linspace(0.5,9.5,10)
fig = plt.figure(1,figsize=(12,6))

ax = fig.add_subplot(111)

ax.bar(ind,quants,width,color='coral')

ax.set_xticks(ind)
ax.set_xticklabels(labels)

# ax.set_yticks(quants)
# ax.set_yticklabels(quants)


ax.set_xlabel('Country')
ax.set_ylabel('GDP (Billion US dollar)')
ax.set_title('Top 10 GDP Countries',bbox={'facecolor':'0.8','pad':5})
plt.show()

