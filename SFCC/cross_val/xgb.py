import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

train_data_df = pd.read_csv('train_cat.csv',delimiter=',',header = 0)
test_data_df = pd.read_csv('test_cat.csv',header = 0 ,delimiter=",")

labels_numeric = pd.Series(train_data_df['crime'],dtype = "category")
train_data_df = train_data_df.drop('crime',1)

train_columns = train_data_df.columns
test_columns = test_data_df.columns

enc = LabelEncoder()

for col in train_columns :	
	if col == 'hour' or col == 'day' or col == 'county' :		
		train_data_df[col] = enc.fit_transform(train_data_df[col])

for col in test_columns :	
	if col == 'hour' or col == 'day' or col == 'county' :
		train_data_df[col] = enc.fit_transform(train_data_df[col])

xg_train = xgb.DMatrix(train_data_df,label=labels_numeric)
xg_test = xgb.DMatrix(test_data_df)

param = {}
param['objective'] = 'multi:softprob'
param['eta'] = 0.1
param['max_depth'] = 6
param['max_delta_step'] = 5
param['min_child_weight'] = 5
param['subsample'] = 0.85
param['colsample_bytree'] = 0.65
param['num_class'] = 39
num_round = 20

gbm = xgb.train(param,xg_train,num_round)
test_pred = gbm.predict(xg_test,output_margin = True)

crimes = {'24': 'TRESPASS', '25': 'LARCENY/THEFT', '26': 'VANDALISM', '27': 'NON-CRIMINAL', '20': 'RECOVERED VEHICLE', '21': 'FRAUD', '22': 'ARSON', '23': 'DRUG/NARCOTIC', '28': 'EXTORTION', '29': 'PORNOGRAPHY/OBSCENE MAT', '1': 'WEAPON LAWS', '0': 'KIDNAPPING', '3': 'WARRANTS', '2': 'SECONDARY CODES', '5': 'EMBEZZLEMENT', '4': 'PROSTITUTION', '7': 'SUICIDE', '6': 'LOITERING', '9': 'SEX OFFENSES FORCIBLE', '8': 'DRIVING UNDER THE INFLUENCE', '38': 'RUNAWAY', '11': 'BURGLARY', '10': 'ROBBERY', '13': 'FAMILY OFFENSES', '12': 'SUSPICIOUS OCC', '15': 'FORGERY/COUNTERFEITING', '14': 'BRIBERY', '17': 'DRUNKENNESS', '16': 'BAD CHECKS', '19': 'OTHER OFFENSES', '18': 'GAMBLING', '31': 'SEX OFFENSES NON FORCIBLE', '30': 'LIQUOR LAWS', '37': 'DISORDERLY CONDUCT', '36': 'MISSING PERSON', '35': 'ASSAULT', '34': 'STOLEN PROPERTY', '33': 'VEHICLE THEFT', '32': 'TREA'}

labels = labels_numeric.tolist()

fId = open('IDs.txt')
id_list = []
for i in fId :
	j = i.strip()
	id_list.append(j)

predictions = []
for i in test_pred :	
	dic = {}
	for j in range(len(i)) :
		dic[i[j]] = labels[j]
	k = sorted(i,reverse=True)[0]
	predictions.append(crimes[str(dic[k])]) 

col_names = ['Id','ARSON','ASSAULT','BAD CHECKS','BRIBERY','BURGLARY','DISORDERLY CONDUCT','DRIVING UNDER THE INFLUENCE','DRUG/NARCOTIC','DRUNKENNESS','EMBEZZLEMENT','EXTORTION','FAMILY OFFENSES','FORGERY/COUNTERFEITING','FRAUD','GAMBLING','KIDNAPPING','LARCENY/THEFT','LIQUOR LAWS','LOITERING','MISSING PERSON','NON-CRIMINAL','OTHER OFFENSES','PORNOGRAPHY/OBSCENE MAT','PROSTITUTION','RECOVERED VEHICLE','ROBBERY','RUNAWAY','SECONDARY CODES','SEX OFFENSES FORCIBLE','SEX OFFENSES NON FORCIBLE','STOLEN PROPERTY','SUICIDE','SUSPICIOUS OCC','TREA','TRESPASS','VANDALISM','VEHICLE THEFT','WARRANTS','WEAPON LAWS']

f = open('results_oneHot.csv','w')
f.write(','.join(col_names)+'\n')
for i in range(len(predictions)) :
	j = [0 for k in range(40)]
	j[0] = id_list[i]
	pred = predictions[i]
	ind = col_names.index(pred)
	j[ind] += 1
	f.write(','.join(str(p) for p in j)+'\n')
