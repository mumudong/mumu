import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import LogisticRegressionCV,LogisticRegression
import statsmodels.api as sm
from sklearn.ensemble import RandomForestClassifier
from numpy import log
import numpy as np
from sklearn.metrics import roc_auc_score,f1_score,recall_score
from scorecard_functions_V3 import *

# 数据预处理
# 1，读入数据
# 2，选择合适的建模样本
# 3，数据集划分成训练集和测试集

folderOfData = 'pickle文件/'

allData = pd.read_csv('application.csv',header = 0, encoding = 'latin1')
allData['term'] = allData['term'].apply(lambda x: int(x.replace(' months','')))

# 处理标签：Fully Paid是正常用户；Charged Off是违约用户
allData['y'] = allData['loan_status'].map(lambda x: int(x == 'Charged Off'))

'''
由于存在不同的贷款期限（term），申请评分卡模型评估的违约概率必须要在统一的期限中，且不宜太长，所以选取term＝36months的行本
'''

allData1 = allData.loc[allData.term == 36]

trainData, testData = train_test_split(allData1,test_size=0.3)

#固化变量
trainDataFile = open(folderOfData+'trainData.pkl','wb')
pickle.dump(trainData, trainDataFile)
trainDataFile.close()

testDataFile = open(folderOfData+'testData.pkl','wb')
pickle.dump(testData, testDataFile)
testDataFile.close()

'''
第一步：数据预处理，包括
（1）数据清洗
（2）格式转换
（3）缺失值填补
'''

# 将带％的百分比变为浮点数
trainData['int_rate_clean'] = trainData['int_rate'].map(lambda x: float(x.replace('%',''))/100)

# 将工作年限进行转化，否则影响排序
trainData['emp_length_clean'] = trainData['emp_length'].astype(str).map(CareerYear)

# 将desc的缺失作为一种状态，非缺失作为另一种状态
trainData['desc_clean'] = trainData['desc'].map(DescExisting)

# 处理日期。earliest_cr_line的格式不统一，需要统一格式且转换成python的日期
trainData['app_date_clean'] = trainData['issue_d'].map(lambda x: ConvertDateStr(x))
trainData['earliest_cr_line_clean'] = trainData['earliest_cr_line'].map(lambda x: ConvertDateStr(x))

# 处理mths_since_last_delinq。注意原始值中有0，所以用－1代替缺失
trainData['mths_since_last_delinq_clean'] = trainData['mths_since_last_delinq'].map(lambda x:MakeupMissing(x))

trainData['mths_since_last_record_clean'] = trainData['mths_since_last_record'].map(lambda x:MakeupMissing(x))

trainData['pub_rec_bankruptcies_clean'] = trainData['pub_rec_bankruptcies'].map(lambda x:MakeupMissing(x))

'''
第二步：变量衍生
'''
# 考虑申请额度与收入的占比
trainData['limit_income'] = trainData.apply(lambda x: x.loan_amnt / x.annual_inc, axis = 1)

# 考虑earliest_cr_line到申请日期的跨度，以月份记
trainData['earliest_cr_to_app'] = trainData.apply(lambda x: MonthGap(x.earliest_cr_line_clean,x.app_date_clean), axis = 1)

'''
第三步：分箱，采用ChiMerge,要求分箱完之后：
（1）不超过5箱
（2）Bad Rate单调
（3）每箱同时包含好坏样本
（4）特殊值如－1，单独成一箱

连续型变量可直接分箱
类别型变量：
（a）当取值较多时，先用bad rate编码，再用连续型分箱的方式进行分箱
（b）当取值较少时：
    （b1）如果每种类别同时包含好坏样本，无需分箱
    （b2）如果有类别只包含好坏样本的一种，需要合并
'''
#数值型变量
num_features = ['int_rate_clean','emp_length_clean','annual_inc', 'dti', 'delinq_2yrs', 'earliest_cr_to_app','inq_last_6mths', \
                'mths_since_last_record_clean', 'mths_since_last_delinq_clean','open_acc','pub_rec','total_acc','limit_income','earliest_cr_to_app']
#类型型变量
cat_features = ['home_ownership', 'verification_status','desc_clean', 'purpose', 'zip_code','addr_state','pub_rec_bankruptcies_clean']

more_value_features = [] # 类别变量，取值超过5
less_value_features = [] # 取值小于5
# 第一步，检查类别型变量中，哪些变量取值超过5
for var in cat_features:
    valueCounts = len(set(trainData[var]))
    print(valueCounts)
    if valueCounts > 5:
        more_value_features.append(var)  #取值超过5的变量，需要bad rate编码，再用卡方分箱法进行分箱
    else:
        less_value_features.append(var)

# （i）当取值<5时：如果每种类别同时包含好坏样本，无需分箱；如果有类别只包含好坏样本的一种，需要合并
merge_bin_dict = {}  # 存放需要合并的变量，以及合并方法
var_bin_list = []   # 由于某个取值没有好或者坏样本而需要合并的变量
for col in less_value_features:
    binBadRate = BinBadRate(trainData, col, 'y')[0]
    if min(binBadRate.values()) == 0 :  # 由于某个取值没有坏样本而进行合并
        print('{} need to be combined due to 0 bad rate'.format(col))
        combine_bin = MergeBad0(trainData, col, 'y') # 获取新的类别分箱
        merge_bin_dict[col] = combine_bin
        newVar = col + '_Bin'
        trainData[newVar] = trainData[col].map(combine_bin)
        var_bin_list.append(newVar)
    if max(binBadRate.values()) == 1:    #由于某个取值没有好样本而进行合并
        print('{} need to be combined due to 0 good rate'.format(col))
        combine_bin = MergeBad0(trainData, col, 'y',direction = 'good')
        merge_bin_dict[col] = combine_bin
        newVar = col + '_Bin'
        trainData[newVar] = trainData[col].map(combine_bin)
        var_bin_list.append(newVar)

#保存merge_bin_dict
file1 = open(folderOfData+'merge_bin_dict.pkl','wb')
pickle.dump(merge_bin_dict,file1)
file1.close()


#less_value_features里剩下不需要合并的变量
less_value_features = [i for i in less_value_features if i + '_Bin' not in var_bin_list]

# （ii）当取值>5时：用bad rate进行编码，放入连续型变量里
br_encoding_dict = {}   #记录按照bad rate进行编码的变量，及编码方式
for col in more_value_features:
    br_encoding = BadRateEncoding(trainData, col, 'y')
    trainData[col+'_br_encoding'] = br_encoding['encoding']
    br_encoding_dict[col] = br_encoding['bad_rate']
    num_features.append(col+'_br_encoding')

file2 = open(folderOfData+'br_encoding_dict.pkl','wb')
pickle.dump(br_encoding_dict,file2)
file2.close()


# （iii）对连续型变量进行分箱，包括（ii）中的变量
continous_merged_dict = {}
for col in num_features:
    print("{} is in processing".format(col))
    if -1 not in set(trainData[col]):   #－1会当成特殊值处理。如果没有－1，则所有取值都参与分箱
        max_interval = 5   #分箱后的最多的箱数
        cutOff = ChiMerge(trainData, col, 'y', max_interval=max_interval,special_attribute=[],minBinPcnt=0)
        trainData[col+'_Bin'] = trainData[col].map(lambda x: AssignBin(x, cutOff,special_attribute=[]))
        monotone = BadRateMonotone(trainData, col+'_Bin', 'y')   # 检验分箱后的单调性是否满足
        while(not monotone):
            # 检验分箱后的单调性是否满足。如果不满足，则缩减分箱的个数。
            max_interval -= 1
            cutOff = ChiMerge(trainData, col, 'y', max_interval=max_interval, special_attribute=[],
                              minBinPcnt=0)
            trainData[col + '_Bin'] = trainData[col].map(lambda x: AssignBin(x, cutOff, special_attribute=[]))
            if max_interval == 2:
                # 当分箱数为2时，必然单调
                break
            monotone = BadRateMonotone(trainData, col + '_Bin', 'y')
        newVar = col + '_Bin'
        trainData[newVar] = trainData[col].map(lambda x: AssignBin(x, cutOff, special_attribute=[]))
        var_bin_list.append(newVar)
    else:
        max_interval = 5
        # 如果有－1，则除去－1后，其他取值参与分箱
        cutOff = ChiMerge(trainData, col, 'y', max_interval=max_interval, special_attribute=[-1],
                          minBinPcnt=0)
        trainData[col + '_Bin'] = trainData[col].map(lambda x: AssignBin(x, cutOff, special_attribute=[-1]))
        monotone = BadRateMonotone(trainData, col + '_Bin', 'y',['Bin -1'])
        while (not monotone):
            max_interval -= 1
            # 如果有－1，－1的bad rate不参与单调性检验
            cutOff = ChiMerge(trainData, col, 'y', max_interval=max_interval, special_attribute=[-1],
                              minBinPcnt=0)
            trainData[col + '_Bin'] = trainData[col].map(lambda x: AssignBin(x, cutOff, special_attribute=[-1]))
            if max_interval == 3:
                # 当分箱数为3-1=2时，必然单调
                break
            monotone = BadRateMonotone(trainData, col + '_Bin', 'y',['Bin -1'])
        newVar = col + '_Bin'
        trainData[newVar] = trainData[col].map(lambda x: AssignBin(x, cutOff, special_attribute=[-1]))
        var_bin_list.append(newVar)
    continous_merged_dict[col] = cutOff

file3 = open(folderOfData+'continous_merged_dict.pkl','wb')
pickle.dump(continous_merged_dict,file3)
file3.close()


'''
第四步：WOE编码、计算IV
'''
WOE_dict = {}
IV_dict = {}
# 分箱后的变量进行编码，包括：
# 1，初始取值个数小于5，且不需要合并的类别型变量。存放在less_value_features中,原始列名
# 2，初始取值个数小于5，需要合并的类别型变量。合并后新的变量存放在var_bin_list中，后缀 _Bin
# 3，初始取值个数超过5，需要合并的类别型变量。合并后新的变量列名_br_encoding，先存放连续变量中，卡方分箱后加_Bin存放在var_bin_list中
# 4，连续变量。分箱后新的变量存放在var_bin_list中
all_var = var_bin_list  + less_value_features
for var in all_var:
    woe_iv = CalcWOE(trainData, var, 'y')
    WOE_dict[var] = woe_iv['WOE']
    IV_dict[var] = woe_iv['IV']


file4 = open(folderOfData+'WOE_dict.pkl','wb')
pickle.dump(WOE_dict,file4)
file4.close()


#将变量IV值进行降序排列，方便后续挑选变量
IV_dict_sorted = sorted(IV_dict.items(), key=lambda x: x[1], reverse=True)

IV_values = [i[1] for i in IV_dict_sorted]
IV_name = [i[0] for i in IV_dict_sorted]
plt.title('feature IV')
plt.bar(range(len(IV_values)),IV_values)
plt.show()



'''
第五步：单变量分析和多变量分析，均基于WOE编码后的值。
（1）选择IV高于0.01的变量
（2）比较两两线性相关性。如果相关系数的绝对值高于阈值，剔除IV较低的一个
'''

#选取IV>0.01的变量
high_IV = {k:v for k, v in IV_dict.items() if v >= 0.02}
high_IV_sorted = sorted(high_IV.items(),key=lambda x:x[1],reverse=True)

short_list = high_IV.keys()
short_list_2 = []
for var in short_list:
    newVar = var + '_WOE'
    trainData[newVar] = trainData[var].map(WOE_dict[var])
    short_list_2.append(newVar)

#对于上一步的结果，计算相关系数矩阵，并画出热力图进行数据可视化
trainDataWOE = trainData[short_list_2]
f, ax = plt.subplots(figsize=(10, 8))
corr = trainDataWOE.corr()
sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),square=True, ax=ax)
plt.show()

#两两间的线性相关性检验
#1，将候选变量按照IV进行降序排列
#2，计算第i和第i+1的变量的线性相关系数
#3，对于系数超过阈值的两个变量，剔除IV较低的一个
deleted_index = []
cnt_vars = len(high_IV_sorted)
for i in range(cnt_vars):
    if i in deleted_index:
        continue
    x1 = high_IV_sorted[i][0]+"_WOE"
    for j in range(cnt_vars):
        if i == j or j in deleted_index:
            continue
        y1 = high_IV_sorted[j][0]+"_WOE"
        roh = np.corrcoef(trainData[x1],trainData[y1])[0,1]
        if abs(roh)>0.7:
            x1_IV = high_IV_sorted[i][1]
            y1_IV = high_IV_sorted[j][1]
            if x1_IV > y1_IV:
                deleted_index.append(j)
            else:
                deleted_index.append(i)

multi_analysis_vars_1 = [high_IV_sorted[i][0]+"_WOE" for i in range(cnt_vars) if i not in deleted_index]


'''
多变量分析：VIF
'''
X = np.matrix(trainData[multi_analysis_vars_1])
VIF_list = [variance_inflation_factor(X, i) for i in range(X.shape[1])]
max_VIF = max(VIF_list)
print(max_VIF)
# 最大的VIF是1.32267733123，一般小于9认为无关，因此这一步认为没有多重共线性
multi_analysis = multi_analysis_vars_1



'''
第六步：逻辑回归模型。
要求：
1，变量显著
2，符号为负
'''
### (1)将多变量分析的后变量带入LR模型中
y = trainData['y']
X = trainData[multi_analysis]
X['intercept'] = [1]*X.shape[0]


LR = sm.Logit(y, X).fit()
summary = LR.summary()
pvals = LR.pvalues
pvals = pvals.to_dict()
print('pvals --> ',{k: v for k,v in pvals.items()})
# ### 有些变量不显著，需要逐步剔除
varLargeP = {k: v for k,v in pvals.items() if v >= 0.1}
varLargeP = sorted(varLargeP.items(), key=lambda d:d[1], reverse = True)
print('varLarge === ',varLargeP)
while(len(varLargeP) > 0 and len(multi_analysis) > 0):
    # 每次迭代中，剔除最不显著的变量，直到
    # (1) 剩余所有变量均显著
    # (2) 没有特征可选
    varMaxP = varLargeP[0][0]
    print('varMaxP --> ',varMaxP)
    if varMaxP == 'intercept':
        print('the intercept is not significant!')
        break
    multi_analysis.remove(varMaxP)
    y = trainData['y']
    X = trainData[multi_analysis]
    X['intercept'] = [1] * X.shape[0]

    LR = sm.Logit(y, X).fit()
    pvals = LR.pvalues
    pvals = pvals.to_dict()
    varLargeP = {k: v for k, v in pvals.items() if v >= 0.1}
    varLargeP = sorted(varLargeP.items(), key=lambda d: d[1], reverse=True)
    print('varLargeP --> ',varLargeP)
summary = LR.summary()
print('summary:\n',summary)
# 保存变量
saveModel =open(folderOfData+'var_in_model.pkl','wb')
pickle.dump(LR.pvalues.index,saveModel)
saveModel.close()

"""
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                      y   No. Observations:                17457
Model:                          Logit   Df Residuals:                    17448
Method:                           MLE   Df Model:                            8
Date:                Thu, 21 Dec 2017   Pseudo R-squ.:                  0.1088
Time:                        10:47:03   Log-Likelihood:                -5375.7
converged:                       True   LL-Null:                       -6031.8
                                        LLR p-value:                5.366e-278
========================================================================================================
                                           coef    std err          z      P>|z|      [0.025      0.975]
--------------------------------------------------------------------------------------------------------
zip_code_br_encoding_Bin_WOE            -0.9917      0.041    -23.989      0.000      -1.073      -0.911
int_rate_clean_Bin_WOE                  -0.9261      0.056    -16.569      0.000      -1.036      -0.817
annual_inc_Bin_WOE                      -0.7620      0.095     -8.038      0.000      -0.948      -0.576
purpose_br_encoding_Bin_WOE             -0.8410      0.103     -8.131      0.000      -1.044      -0.638
inq_last_6mths_Bin_WOE                  -0.7636      0.111     -6.908      0.000      -0.980      -0.547
mths_since_last_record_clean_Bin_WOE    -0.7934      0.134     -5.942      0.000      -1.055      -0.532
limit_income_Bin_WOE                    -0.5277      0.147     -3.583      0.000      -0.816      -0.239
emp_length_clean_Bin_WOE                -0.8358      0.171     -4.894      0.000      -1.171      -0.501
intercept                               -2.0969      0.027    -78.744      0.000      -2.149      -2.045
========================================================================================================
"""


# trainData['prob'] = LR.predict(X)
# regressionModel = LogisticRegression().fit(X,y)
# trainData['probility'] = regressionModel.predict(X)
# print(trainData[['score']].head())
# auc = roc_auc_score(trainData['y'],trainData['prob'])  #AUC = 0.73
# f1score = f1_score(trainData['y'],trainData['score'])
# recall = recall_score(trainData['y'],trainData['score'])
# print(' auc----> ',auc)
# print(' f1score --> ',f1score)
# print(' recall --> ',recall)


#将模型保存
# saveModel =open(folderOfData+'LR_Model_Normal.pkl','wb')
# pickle.dump(LR,saveModel)
# saveModel.close()


#############################################################################################################
#尝试用L1约束#
## use cross validation to select the best regularization parameter

multi_analysis = multi_analysis_vars_1
X = trainData[multi_analysis]   #by default  LogisticRegressionCV() fill fit the intercept
X = np.matrix(X)
y = trainData['y']
y = np.array(y)
sns.countplot(trainData['y'])
plt.xlabel('class')
plt.ylabel('number')
plt.title('classWeight')
plt.show()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
X_train.shape, y_train.shape
#
# model_parameter = {}
# for C_penalty in np.arange(0.005, 0.2,0.005):
#     for bad_weight in range(2, 101, 2):
#         print(C_penalty, bad_weight)
#         #使用交叉验证来选择正则化系数C
#         LR_model_2 = LogisticRegressionCV(Cs=[C_penalty], penalty='l2', solver='lbfgs', class_weight={1:bad_weight, 0:1})
#         LR_model_2_fit = LR_model_2.fit(X_train,y_train)
#         y_pred = LR_model_2_fit.predict_proba(X_test)[:,1]
#         scorecard_result = pd.DataFrame({'prob':y_pred, 'target':y_test})
#         performance = KS(scorecard_result,'prob','target')
#         # KS = performance['KS']
#         # KS = performance
#         model_parameter[(C_penalty, bad_weight)] = performance #KS
# sortparam = sorted(model_parameter,key=lambda x:x[1],reverse=True)
# print('sortedparam --> ',sortparam[0],model_parameter[sortparam[0]],sortparam[1],model_parameter[sortparam[0]])
# penalty,badWeight = sortparam[0]
LR_model_2 = LogisticRegressionCV(penalty='l2', solver='lbfgs')
LR_model_2_fit = LR_model_2.fit(X_train,y_train)
y_prob = LR_model_2_fit.predict_proba(X_test)[:,1]
print('y_prob --> ',y_prob.shape)
y_pred = LR_model_2_fit.predict(X_test)
print('y_pred --> ',y_pred.shape)
scorecard_result = pd.DataFrame({'prob':y_prob, 'target':y_test,'pred':y_pred})
performance = KS(scorecard_result,'prob','target')
print('ks --> ',performance)
print('auc --> ',roc_auc_score(scorecard_result['target'],scorecard_result['prob']))
print(' f1score --> ',f1_score(scorecard_result['target'],scorecard_result['pred']))
print(' recall --> ',recall_score(scorecard_result['target'],scorecard_result['pred']))
# auc = roc_auc_score(testData['y'],testData['prob'])
# ks = KS(testData, 'prob', 'y')
# endtime = datetime.datetime.now()
# print (endtime - starttime).seconds
#将模型保存
saveModel =open(folderOfData+'LR_Model_Normal.pkl','wb')
pickle.dump(LR_model_2_fit,saveModel)
saveModel.close()
print('模型变量:',list(LR.pvalues.index))
print('模型变量:',multi_analysis)
'''
# 用随机森林法估计变量重要性#
#
var_WOE_list = multi_analysis_vars_1
X = trainData[var_WOE_list]
X = np.matrix(X)
y = trainData['y']
y = np.array(y)

RFC = RandomForestClassifier()
RFC_Model = RFC.fit(X,y)
features_rfc = trainData[var_WOE_list].columns
featureImportance = {features_rfc[i]:RFC_Model.feature_importances_[i] for i in range(len(features_rfc))}
featureImportanceSorted = sorted(featureImportance.items(),key=lambda x: x[1], reverse=True)
# we selecte the top 10 features
features_selection = [k[0] for k in featureImportanceSorted[:8]]

y = trainData['y']
X = trainData[features_selection]
X['intercept'] = [1]*X.shape[0]


LR = sm.Logit(y, X).fit()
summary = LR.summary()
'''




