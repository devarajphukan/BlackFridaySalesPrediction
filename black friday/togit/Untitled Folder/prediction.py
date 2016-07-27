import pandas as pd 
import numpy as np 
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import xgboost as xgb

def clean_my_df(fileName):

	lbl_enc = LabelEncoder()
	oh_enc = OneHotEncoder()

	def LabelEncoding(col):
		lbl_enc.fit(col)
		cat_col = lbl_enc.transform(col)
		return cat_col

	def OneHotEncoding(col):
		oh_enc.fit(col)
		cat_col = oh_enc.transform(col)
		return cat_col

	df = pd.read_csv(fileName)
	# print df.columns
	df = df.drop(['User_ID','Product_ID'],axis = 1)
	
	try :
		df = df.drop(['Comb'],axis = 1)
	except :
		pass

	cat_cols = ['Gender','Age','Occupation','City_Category','Stay_In_Current_City_Years','Marital_Status']

	df_new = df.drop(['Gender','Age','Occupation','City_Category','Stay_In_Current_City_Years','Marital_Status'],axis = 1)

	for c in cat_cols :
		data = pd.DataFrame({c:LabelEncoding(df[c])})
		df_new = pd.concat([df_new,data],axis = 1)

	df_new_oh = df_new.drop(['Gender','Age','Occupation','City_Category','Stay_In_Current_City_Years','Marital_Status'],axis = 1)

	for c in cat_cols :
		data = pd.DataFrame({c:LabelEncoding(df_new[c])})
		df_new_oh = pd.concat([df_new_oh,data],axis = 1)

	return df_new_oh

train_df = clean_my_df('train.csv')
# print train_df.columns
purchases = train_df['Purchase']
train_df = train_df.drop(['Purchase'],axis = 1)

test_df = clean_my_df('test.csv')
# print test_df.columns
test_df = test_df.drop(test_df.columns[0],axis = 1)
# print purchases
xg_train = xgb.DMatrix(train_df,label=np.array(purchases),missing=np.nan)
xg_test = xgb.DMatrix(test_df,missing=np.nan)

param = {}
param['objective'] = 'reg:linear'
param['eval_metric'] = 'rmse'
param['eta'] = 0.01
param['gamma'] = 0.1
param['min_child_weight'] = 9
param['max_depth'] = 6
# param['subsample'] = 0.85
# param['colsample_bytree'] = 0.85
param['lambda'] = 1
param['alpha'] = 1
num_round = 2000

gbm = xgb.train(param,xg_train,num_round)
test_pred = gbm.predict(xg_test)

s = open('submitFile').read()
ss = s.split("\n")
f = open("submission.csv","w")
f.write("User_ID,Product_ID,Purchase\n")
for i in range(len(test_pred)) :
	wr = ss[i]+","+str(test_pred[i])+"\n"
	f.write(wr)

