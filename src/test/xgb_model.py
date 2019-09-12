from sklearn.model_selection import train_test_split, cross_validate
from sklearn.metrics import mean_squared_error
import pickle
import xgboost as xgb
#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv("data.csv")
labels = ['rh', 'temp']

X_train, X_test, y_tr, y_te = train_test_split(data[labels], data['co2'], test_size=0.01, random_state=0)
y_train = y_tr.values.reshape((y_tr.shape[0],1))
y_test = y_te.values.reshape((y_te.shape[0],1))
print(X_train.shape, X_test.shape)


xg = xgb.XGBRegressor(objective ='reg:linear', colsample_bytree = 0.3, learning_rate = 0.1, max_depth = 6, alpha = 10, n_estimators = 1000, n_jobs=-1)
X_train = X_train.as_matrix()
X_test = X_test.as_matrix()

xg.fit(X_train, y_train)

preds = xg.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, preds))
print("RMSE: %f" % (rmse))
preds = xg.predict(data[labels])
'''
plt.plot(preds)
plt.plot(data['co2'])
plt.show()
'''
'''
params = {"objective":"reg:linear",'colsample_bytree': 0.3,'learning_rate': 0.1, 'max_depth': 6, 'alpha': 10}

dmatrix = xgb.DMatrix(data=data[labels],label=data['co2']) 
cv_results = xgb.cv(dtrain=dmatrix, params=params, nfold=5,num_boost_round=100,early_stopping_rounds=5,metrics="rmse", as_pandas=True, seed=123)
'''
