import numpy as np
import pandas as pd
#创建series的方式
s1 = pd.Series([1,2,3,4])
s2 = pd.Series(np.arange(6))
s3 = pd.Series({'1':1,'2':2})
s4 = pd.Series([1,2,3,4],index=['a','b','c','d'])
print(s4)