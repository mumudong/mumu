import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import LogisticRegressionCV
import statsmodels.api as sm
from sklearn.ensemble import RandomForestClassifier
from numpy import log
import numpy as np
from sklearn.metrics import roc_auc_score,roc_curve,auc
from scorecard_functions_V3 import *
class ScoreModel:

    def __init__(self):
        folderOfData = 'pickle文件/'
        # 获取模型
        modelFile =open(folderOfData+'LR_Model_Normal.pkl','rb')
        self.LR = pickle.load(modelFile)
        modelFile.close()
        #对变量的处理只需针对入模变量即可
        modelFile =open(folderOfData+'var_in_model.pkl','rb')
        self.var_in_model = pickle.load(modelFile)
        modelFile.close()
        print('var_in_model---->',self.var_in_model)
        self.var_in_model.remove('intercept')
        # 获取分箱字典
        file1 = open(folderOfData+'merge_bin_dict.pkl','rb')
        self.merge_bin_dict = pickle.load(file1)
        file1.close()
        # 获取badrate encoding字典
        file2 = open(folderOfData+'br_encoding_dict.pkl','rb')
        self.br_encoding_dict = pickle.load(file2)
        file2.close()
        # 获取分箱字典
        file3 = open(folderOfData+'continous_merged_dict.pkl','rb')
        self.continous_merged_dict = pickle.load(file3)
        file3.close()
        # 获取分箱woe编码字典
        file4 = open(folderOfData+'WOE_dict.pkl','rb')
        self.WOE_dict = pickle.load(file4)
        file4.close()
        # 定义基础分
        self.oddso = 1/60
        self.basePoint = 600
        self.PDO = 20
        self.B = self.PDO/np.log(2)
        self.A = self.basePoint + self.B * np.log(self.oddso)
        # 定义数据框列
        self.cols = "member_id,loan_amnt,term,loan_status,int_rate,emp_length,home_ownership,annual_inc,verification_status,desc,purpose,title,zip_code,addr_state,dti,delinq_2yrs,inq_last_6mths,mths_since_last_delinq,mths_since_last_record,open_acc,pub_rec,total_acc,pub_rec_bankruptcies,issue_d,earliest_cr_line".split(',')
        print('***************************** Init complete *****************************')
    def ModifyDf(self,x, new_value):
        if np.isnan(x):
            return new_value
        else:
            return x

    def Prob2Score(self,prob):
        #将概率转化成分数且为正整数
        y = np.log(prob/(1-prob))
        return int(self.A - self.B * y)

    def convertType(self,s,itype):
        if itype == 'int64':
            if s == "":
                return np.nan
            else:
                return np.int64(s)
        if itype == 'float64':
            if s == "":
                return np.nan
            else:
                return np.float64(s)
        return np.nan
    def getScore(self,record):
        testData = pd.DataFrame(np.array(record.split(',')).reshape(1,25),columns=self.cols)
        testData['member_id'] = testData['member_id'].map(lambda x:self.convertType(x,'int64'))
        testData['loan_amnt'] = testData['loan_amnt'].map(lambda x:self.convertType(x,'int64'))
        testData['annual_inc'] = testData['annual_inc'].map(lambda x:self.convertType(x,'float64'))
        testData['dti'] = testData['dti'].map(lambda x:self.convertType(x,'float64'))
        testData['delinq_2yrs'] = testData['delinq_2yrs'].map(lambda x:self.convertType(x,'int64'))
        testData['inq_last_6mths'] = testData['inq_last_6mths'].map(lambda x:self.convertType(x,'int64'))
        testData['mths_since_last_delinq'] = testData['mths_since_last_delinq'].map(lambda x:self.convertType(x,'float64'))
        testData['mths_since_last_record'] = testData['mths_since_last_record'].map(lambda x:self.convertType(x,'float64'))
        testData['open_acc'] = testData['open_acc'].map(lambda x:self.convertType(x,'int64'))
        testData['pub_rec'] = testData['pub_rec'].map(lambda x:self.convertType(x,'int64'))
        testData['total_acc'] = testData['total_acc'].map(lambda x:self.convertType(x,'int64'))
        testData['pub_rec_bankruptcies'] = testData['pub_rec_bankruptcies'].map(lambda x:self.convertType(x,'float64'))
        # 第一步：完成数据预处理
        # 将带％的百分比变为浮点数
        testData['int_rate_clean'] = testData['int_rate'].map(lambda x: float(x.replace('%',''))/100)
        # 将工作年限进行转化，否则影响排序
        testData['emp_length_clean'] = testData['emp_length'].astype(str).map(CareerYear)
        # 将desc的缺失作为一种状态，非缺失作为另一种状态
        testData['desc_clean'] = testData['desc'].map(DescExisting)
        # 处理日期。earliest_cr_line的格式不统一，需要统一格式且转换成python的日期
        testData['app_date_clean'] = testData['issue_d'].map(lambda x: ConvertDateStr(x))
        testData['earliest_cr_line_clean'] = testData['earliest_cr_line'].map(lambda x: ConvertDateStr(x))
        # 处理mths_since_last_delinq。注意原始值中有0，所以用－1代替缺失
        testData['mths_since_last_delinq_clean'] = testData['mths_since_last_delinq'].map(lambda x:MakeupMissing(x))
        testData['mths_since_last_record_clean'] = testData['mths_since_last_record'].map(lambda x:MakeupMissing(x))
        testData['pub_rec_bankruptcies_clean'] = testData['pub_rec_bankruptcies'].map(lambda x:MakeupMissing(x))

        # 第二步：变量衍生
        # 考虑申请额度与收入的占比
        testData['limit_income'] = testData.apply(lambda x: x.loan_amnt / x.annual_inc, axis = 1)
        # 考虑earliest_cr_line到申请日期的跨度，以月份记
        testData['earliest_cr_to_app'] = testData.apply(lambda x: MonthGap(x.earliest_cr_line_clean,x.app_date_clean), axis = 1)

        # 第三步：分箱并代入WOE值
        for var in self.var_in_model:
            var1 = var.replace('_Bin_WOE','')

            # 有些取值个数少、但是需要合并的变量
            if var1 in self.merge_bin_dict.keys():
                testData[var1 + '_Bin'] = testData[var1].map(self.merge_bin_dict[var1])
            # 有些变量需要用bad rate进行编码
            if var1.find('_br_encoding')>-1:
                var2 =var1.replace('_br_encoding','')
                testData[var1] = testData[var2].map(self.br_encoding_dict[var2])
                #需要注意的是，有可能在测试样中某些值没有出现在训练样本中，从而无法得出对应的bad rate是多少。故可以用最坏（即最大）的bad rate进行编码
                max_br = max(testData[var1])
                testData[var1] = testData[var1].map(lambda x: self.ModifyDf(x, max_br))
            #上述处理后，需要加上连续型变量一起进行分箱
            if var1 in set(self.continous_merged_dict.keys()):
                if -1 not in set(testData[var1]):
                    testData[var1+'_Bin'] = testData[var1].map(lambda x: AssignBin(x, self.continous_merged_dict[var1]))
                else:
                    testData[var1 + '_Bin'] = testData[var1].map(lambda x: AssignBin(x, self.continous_merged_dict[var1],[-1]))
            #WOE编码
            var3 = var.replace('_WOE','')
            testData[var] = testData[var3].map(self.WOE_dict[var3])

        #第四步：将WOE值代入LR模型，计算概率和分数

        testData['intercept'] = [1]*testData.shape[0]
        #预测数据集中，变量顺序需要和LR模型的变量顺序一致
        #例如在训练集里，变量在数据中的顺序是“负债比”在“借款目的”之前，对应地，在测试集里，“负债比”也要在“借款目的”之前
        testData2 = testData[self.var_in_model]
        prop = self.LR.predict_proba(testData2)[:,1]
        score = self.Prob2Score(prop)
        id = int(record.split(",")[0])
        return id,score