#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


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


# In[4]:


df= pd.read_csv('E:/thesis files/Pre intervention international.csv')


# In[5]:


df['Date']=pd.to_datetime(df['Date'])
df=df.set_index(df['Date'])


# In[6]:


del df['Date']


# In[11]:


df['AirPassengers']=(df['International Passengers'])/1000000


# In[13]:


del df['International Passengers']


# In[14]:


df.head()


# In[15]:


pre_covid=df


# In[16]:


pre_covid.plot()


# In[17]:


import statsmodels.api as sm
seas_d=sm.tsa.seasonal_decompose(pre_covid.AirPassengers,model='add',period=12);
fig=seas_d.plot()
fig.set_size_inches(15, 8)
plt.show()


# In[18]:


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


# In[19]:


test_stationarity(pre_covid.AirPassengers)


# In[20]:


pre_covid['first_difference'] = pre_covid.AirPassengers - pre_covid.AirPassengers.shift(1)  
test_stationarity(pre_covid.first_difference.dropna(inplace=False))


# In[21]:


pre_covid['seasonal_first_difference'] = pre_covid.first_difference - pre_covid.first_difference.shift(12)  
test_stationarity(df.seasonal_first_difference.dropna(inplace=False))


# In[22]:


fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(pre_covid.seasonal_first_difference.iloc[13:], lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(pre_covid.seasonal_first_difference.iloc[13:], lags=40, ax=ax2)


# In[23]:


mod = sm.tsa.statespace.SARIMAX(pre_covid.AirPassengers, trend='n', order=(0,1,1), seasonal_order=(0,1,1,12))
results = mod.fit()
print (results.summary())


# In[24]:


pre_covid['forecast'] = results.predict(start = 110, end= 121, dynamic= True)  
pre_covid[['AirPassengers', 'forecast']].plot(figsize=(12, 8)) 
plt.savefig('ts_df_predict.png', bbox_inches='tight')


# In[25]:


pre_covid.tail(15)


# In[26]:


from sklearn.metrics import r2_score
y_true = [9.948135,9.461086,9.952955,11.01868,11.644596,11.035622,8.589987,8.6783,8.24063,9.566028,9.135555,7.939127]
y_pred = [9.788763,9.39519,9.711236,10.801818,11.68366,10.924256,8.488317,8.678714,8.317937,9.516519,9.240113,8.179852]
r2_score(y_true, y_pred)


# In[ ]:




