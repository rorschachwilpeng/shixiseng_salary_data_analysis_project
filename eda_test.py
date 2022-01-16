#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 22:01:33 2022

@author: apple
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

df = pd.read_csv('EDA_data.csv')
# remove useless data
i = df[df['avg_salary(month)']==0].index
df = df.drop(i)

# Shanghai df
j = df[df['Job Position(eng)']!='ShangHai'].index
df_shanghai = df.drop(j)
# Beijing df
j = df[df['Job Position(eng)']!='BeiJing'].index
df_beijing = df.drop(j)
# Guangzhou df
j = df[df['Job Position(eng)']!='GuangZhou'].index
df_guangzhou = df.drop(j)

# choose relevent columns
df_shanghai_model = df_shanghai[['avg_salary(month)','Company Size','week_attendence','intern_time_length','Job Position(eng)','Job Acedemic Requiremnt(eng)']]
df_beijing_model = df_beijing[['avg_salary(month)','Company Size','week_attendence','intern_time_length','Job Position(eng)','Job Acedemic Requiremnt(eng)']]
df_guangzhou_model = df_guangzhou[['avg_salary(month)','Company Size','week_attendence','intern_time_length','Job Position(eng)','Job Acedemic Requiremnt(eng)']]


# get dummy data
df_shanghai_dum = pd.get_dummies(df_shanghai_model)
df_beijing_dum = pd.get_dummies(df_beijing_model)
df_guangzhou_dum = pd.get_dummies(df_guangzhou_model)


# train test spilt
X_shanghai = df_shanghai_dum.drop('avg_salary(month)', axis=1)
y_shanghai = df_shanghai_dum['avg_salary(month)'].values
X_train_shanghai, X_test_shanghai, y_train_shanghai, y_test_shanghai = train_test_split(X_shanghai,y_shanghai, test_size=0.2, random_state=42)


# multiple linear regression
import statsmodels.api as sm

X_sm = sm.add_constant(X_shanghai, prepend=False)
model = sm.OLS(y_shanghai, X_sm)
res = model.fit()
#print(res.summary())

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train_shanghai, y_train_shanghai)
#print(lm.predict(X_train_shanghai))

print(np.mean(cross_val_score(lm, X_train_shanghai, y_train_shanghai, scoring = 'neg_mean_absolute_error', cv=9)))
# print(np.mean(cross_val_score(lm, X_train_shanghai, y_train, scoring = 'neg_mean_absolute_error', cv=3)))

# lasso regression
lm_l = Lasso(alpha = .99)
lm_l.fit(X_train_shanghai, y_train_shanghai)
  # after test cv range(2,10), when cv=8 turn outs the smallest error
print((np.mean(cross_val_score(lm_l, X_train_shanghai, y_train_shanghai, scoring = 'neg_mean_absolute_error', cv=9))))


alpha = []
error = []

for i in range(1,100):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/10))
    error.append(np.mean(cross_val_score(lml, X_train_shanghai, y_train_shanghai, scoring = 'neg_mean_absolute_error', cv=8)))

plt.plot(alpha, error)

err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns = ['alpha','error'])
  # lasso regression imporve a lot prediction error
print("Optimal alpha for lml: ", df_err[df_err.error == max(df_err.error)])

tpred_lm = lm.predict(X_test_shanghai)
tpred_lml = lm_l.predict(X_test_shanghai)


df_check = pd.DataFrame({'test':y_test_shanghai, 'lm_predicted':tpred_lm, 'lml_predicted':tpred_lml})
