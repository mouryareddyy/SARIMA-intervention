#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
import seaborn as sns
import statsmodels.api as sm  
from statsmodels.tsa.stattools import acf  
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.seasonal import seasonal_decompose


# In[60]:


df= pd.read_csv('E:/thesis files/Pre intervention domestic.csv')


# In[61]:


df['Date']=pd.to_datetime(df['Date'])
df=df.set_index(df['Date'])


# In[62]:


del df['Date']


# In[63]:


df


# In[64]:


df['AirPassengers']=(df['Domestic Passenegers'])/1000000


# In[66]:


del df['Domestic Passenegers']


# In[67]:


df.head()


# In[68]:


pre_covid=df


# In[69]:


pre_covid.plot()


# In[70]:


import statsmodels.api as sm
seas_d=sm.tsa.seasonal_decompose(pre_covid.AirPassengers,model='add',period=12);
fig=seas_d.plot()
fig.set_size_inches(15, 8)
plt.show()


# In[71]:


from statsmodels.tsa.stattools import adfuller
def test_stationarity(timeseries):
    
    #Determing rolling statistics
    rolmean = timeseries.rolling(window=12).mean() # 24 hours on each day
    rolstd = timeseries.rolling(window=12).std()
   

    #Plot rolling statistics:
    fig = plt.figure(figsize=(12, 8))
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()
    
    #Perform Dickey-Fuller test:
    print ('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)


# In[72]:


test_stationarity(pre_covid.AirPassengers)


# In[73]:


pre_covid['first_difference'] = pre_covid.AirPassengers - pre_covid.AirPassengers.shift(1)  
test_stationarity(pre_covid.first_difference.dropna(inplace=False))


# In[74]:


pre_covid['seasonal_first_difference'] = pre_covid.first_difference - pre_covid.first_difference.shift(12)  
test_stationarity(df.seasonal_first_difference.dropna(inplace=False))


# In[75]:


fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(pre_covid.seasonal_first_difference.iloc[13:], lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(pre_covid.seasonal_first_difference.iloc[13:], lags=40, ax=ax2)


# In[78]:


mod = sm.tsa.statespace.SARIMAX(pre_covid.AirPassengers, trend='n', order=(0,1,1), seasonal_order=(0,1,1,12))
results = mod.fit()
print (results.summary())


# In[79]:


pre_covid['forecast'] = results.predict(start = 110, end= 121, dynamic= True)  
pre_covid[['AirPassengers', 'forecast']].plot(figsize=(12, 8)) 
plt.savefig('ts_df_predict.png', bbox_inches='tight')


# In[80]:


pre_covid.tail(15)


# In[83]:


from sklearn.metrics import r2_score
y_true = [70.234011,
66.938177,
71.365029,
72.789897,
75.281255,
72.715566,
63.979337,
69.9223,
64.816897,
69.718631,
61.610609,
59.849933
]
y_pred = [68.594827,
66.207039,
69.493237,
71.723765,
73.822543,
71.660509,
62.895923,
68.99192,
66.307488,
65.872555,
60.373106,
58.147363


]
r2_score(y_true, y_pred)


# In[ ]:




