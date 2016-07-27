import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from time import time
from operator import itemgetter
from scipy.stats import randint as sp_randint
from sklearn.grid_search import GridSearchCV


train_data_df = pd.read_csv('train_cat.csv',delimiter=',',header = 0)
test_data_df = pd.read_csv('test_cat.csv',header = 0 ,delimiter=",")

labels_numeric = pd.Series(train_data_df['crime'],dtype = "category")
train_data_df = train_data_df.drop('crime',1)

train_columns = train_data_df.columns
test_columns = test_data_df.columns

# enc = OneHotEncoder()
enc = LabelEncoder()

for col in train_columns :
	
	if col == 'hour' or col == 'day' or col == 'county' :
		
		train_data_df[col] = enc.fit_transform(train_data_df[col])

for col in test_columns :
	
	if col == 'hour' or col == 'day' or col == 'county' :
		
		train_data_df[col] = enc.fit_transform(train_data_df[col])
		
X = train_data_df
y = labels_numeric

clf = RandomForestClassifier(n_estimators=100)

def report(grid_scores, n_top=3):
	
	top_scores = sorted(grid_scores, key=itemgetter(1), reverse=True)[:n_top]
	for i, score in enumerate(top_scores):
		print("Model with rank: {0}".format(i + 1))
		print("Mean validation score: {0:.3f} (std: {1:.3f})".format(score.mean_validation_score,np.std(score.cv_validation_scores)))
		print("Parameters: {0}".format(score.parameters))
		print("")

param_grid = {"max_depth": [4,6],"max_features":['auto'],"min_samples_split": [6,8],"min_samples_leaf": [3,7],"bootstrap": [True,False]}#,"criterion": ["gini","entropy"]}

# run grid search
grid_search = GridSearchCV(clf, param_grid=param_grid)
start = time()
grid_search.fit(X, y)

print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
      % (time() - start, len(grid_search.grid_scores_)))
report(grid_search.grid_scores_)