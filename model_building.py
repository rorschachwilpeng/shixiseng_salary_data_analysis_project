#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 12:34:03 2022

@author: youtianpeng
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

df = pd.read_csv('EDA_data.csv')
# remove useless data
i = df[df['avg_salary(month)']==0].index
df = df.drop(i)

# choose relevent columns
df_model = df[['avg_salary(month)','Company Size','week_attendence','intern_time_length','Job Position(eng)','Job Acedemic Requiremnt(eng)','Company Field(eng)']]

# get dummy data
df_dum = pd.get_dummies(df_model)

# train test spilt
X = df_dum.drop('avg_salary(month)', axis=1)
y = df_dum['avg_salary(month)'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# multiple linear regression
import statsmodels.api as sm

X_sm = sm.add_constant(X, prepend=False)
model = sm.OLS(y, X_sm)
res = model.fit()
#print(res.summary())

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train, y_train)
#print(lm.predict(X_train))

print(np.mean(cross_val_score(lm, X_train, y_train, scoring = 'neg_mean_absolute_error', cv=9)))
# print(np.mean(cross_val_score(lm, X_train, y_train, scoring = 'neg_mean_absolute_error', cv=3)))

# lasso regression
lm_l = Lasso(alpha = .11)
lm_l.fit(X_train, y_train)
  # after test cv range(2,10), when cv=8 turn outs the smallest error
print((np.mean(cross_val_score(lm_l, X_train, y_train, scoring = 'neg_mean_absolute_error', cv=9))))


alpha = []
error = []

for i in range(1,100):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/10))
    error.append(np.mean(cross_val_score(lml, X_train, y_train, scoring = 'neg_mean_absolute_error', cv=8)))

plt.plot(alpha, error)

err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns = ['alpha','error'])
  # lasso regression imporve a lot prediction error
print("Optimal alpha for lml: ", df_err[df_err.error == max(df_err.error)])

# random forest
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()

print(np.mean(cross_val_score(lml, X_train, y_train, scoring = 'neg_mean_absolute_error', cv=8)))

# tune model GridserachCV
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators': range(10,300,10),
              'criterion': ('gini', 'entropy'),
              'max_features': ('auto','sqrt','log2'),
              'class_weight': ('balanced', 'balanced_subsample')
              }

gs = GridSearchCV(estimator=rf, param_grid=parameters)
gs.fit(X_train, y_train)

print('best score: ',gs.best_score_)
print('best Estimator for the random forest: ',gs.best_estimator_)

gs.best_estimator_


# test ensembles
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
print('lm mse score: ',mean_absolute_error(y_test, tpred_lm))
print('lml mse score: ',mean_absolute_error(y_test, tpred_lml))
print('rf mse score: ',mean_absolute_error(y_test, tpred_rf))



df_check = pd.DataFrame({'test':y_test, 'lm_predicted':tpred_lm, 'lml_predicted':tpred_lml, 'rf_predicted':tpred_rf})


import pickle
pickl = {'model': gs.best_estimator_}
pickle.dump( pickl, open( 'model_file' + ".p", "wb" ) )


file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']
    
model.predict(X_test.iloc[1,:].values.reshape(1,-1))

list(X_test.iloc[1,:])

X_test