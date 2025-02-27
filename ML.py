import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sb 
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import LabelEncoder, StandardScaler 
from sklearn import metrics 
from sklearn.svm import SVC 
from xgboost import XGBRegressor 
from sklearn.linear_model import LinearRegression, Lasso, Ridge 
from sklearn.ensemble import RandomForestRegressor 
from sklearn.metrics import mean_absolute_error as mae 
  
import warnings 
warnings.filterwarnings('ignore')
df = pd.read_csv('StoreDemand.csv') 
display(df.head()) 
display(df.tail())\
parts = df["date"].str.split("-", n = 3, expand = True) 
df["year"]= parts[0].astype('int') 
df["month"]= parts[1].astype('int') 
df["day"]= parts[2].astype('int') 
df.head()
from datetime import datetime 
import calendar 
      
def weekend_or_weekday(year,month,day): 
      
    d = datetime(year,month,day) 
    if d.weekday()>4: 
        return 1
    else: 
        return 0
  
df['weekend'] = df.apply(lambda x:weekend_or_weekday(x['year'], x['month'], x['day']), axis=1) 
df.head()
from datetime import date 
import holidays 
  
def is_holiday(x): 
    
  india_holidays = holidays.country_holidays('IN') 
  
  if india_holidays.get(x): 
    return 1
  else: 
    return 0
  
df['holidays'] = df['date'].apply(is_holiday) 
df.head()

df['m1'] = np.sin(df['month'] * (2 * np.pi / 12)) 
df['m2'] = np.cos(df['month'] * (2 * np.pi / 12)) 
df.head()

def which_day(year, month, day): 
      
    d = datetime(year,month,day) 
    return d.weekday() 
  
df['weekday'] = df.apply(lambda x: which_day(x['year'], 
                                                      x['month'], 
                                                      x['day']), 
                                   axis=1) 
df.head()
df.drop('date', axis=1, inplace=True)
features = ['store', 'year', 'month',\ 
            'weekday', 'weekend', 'holidays'] 
  
plt.subplots(figsize=(20, 10)) 
for i, col in enumerate(features): 
    plt.subplot(2, 3, i + 1) 
    df.groupby(col).mean()['sales'].plot.bar() 
plt.show() 
plt.figure(figsize=(10,5)) 
df.groupby('day').mean()['sales'].plot() 
plt.show()
plt.figure(figsize=(15, 10)) 
  
# Calculating Simple Moving Average  
# for a window period of 30 days 
window_size = 30
data = df[df['year']==2013] 
windows = data['sales'].rolling(window_size) 
sma = windows.mean() 
sma = sma[window_size - 1:] 
  
data['sales'].plot() 
sma.plot() 
plt.legend() 
plt.show()
models = [LinearRegression(), XGBRegressor(), Lasso(), Ridge()] 
  
for i in range(4): 
    models[i].fit(X_train, Y_train) 
  
    print(f'{models[i]} : ') 
  
    train_preds = models[i].predict(X_train) 
    print('Training Error : ', mae(Y_train, train_preds)) 
  
    val_preds = models[i].predict(X_val) 
    print('Validation Error : ', mae(Y_val, val_preds)) 
    print() 
