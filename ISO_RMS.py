#!/usr/bin/env python
# coding: utf-8

# In[52]:


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[53]:


df_mm400 = pd.read_excel("./data/MM400_HF2_5_5_5.xlsx")


# In[54]:


df_nrwm = pd.read_excel("./data/NRWM_HF2_5_5_5.xlsx", sheet_name=1)


# In[55]:


df_mm400.head()


# In[56]:


df_nrwm.head()


# In[57]:


def sq(x):
    return x*x

def findEndOfWeldCandidates(df, field, threshHi, threshLo):
    threshHi = threshHi
    threshLo = threshLo
    sqThreshHi = sq(threshHi)
    sqThreshLo = sq(threshLo)
    mss = 0
    mssHiList = []
    mssLoList = []
    for i in df.index:
        n=i+1
        mss = 1/n * (i*mss + sq(df.loc[i,field]))
        if sq(df.loc[n-1,field])  > mss * sq(threshHi) and sq(df.loc[n,field]) < mss * sq(threshHi):
            mssHiList.append((n,mss))
        if sq(df.loc[n-1,field])  > mss * sq(threshLo) and sq(df.loc[n,field]) < mss * sq(threshLo):
            mssLoList.append((n,mss))
        
    return mssHiList, mssLoList
                            


# In[67]:


def sq(x):
    return x*x

def findEndOfWeldCandidates_PeakCurrentMethod(df, field, threshHi, threshLo):
    threshHi = threshHi
    threshLo = threshLo
    sqThreshHi = sq(threshHi)
    sqThreshLo = sq(threshLo)
    mss = 0
    mssHiList = []
    mssLoList = []
    peak = 0
    for i in df.index:
        n=i+1
        if df.loc[n-1,field] >= peak:
            peak = df.loc[n-1,field]
        mss = 1/n * (i*mss + sq(df.loc[i,field]))
        if df.loc[n-1,field]  > peak * threshHi and df.loc[n,field] < peak * threshHi:
            mssHiList.append((n,mss))
        if df.loc[n-1,field]  > peak * threshLo and df.loc[n,field] < peak * threshLo:
            mssLoList.append((n,mss))
        
    return mssHiList, mssLoList,peak
                            


# In[68]:


def plotResults(df, field, timeField, mssHiList, mssLoList, threshHi, threshLO, ymin, ymax):
    xHi = mssHiList[-1][0]
    yHi = np.sqrt(mssHiList[-1][1])
    xLo = mssLoList[-1][0]
    yLo = np.sqrt(mssLoList[-1][1])

    f, ax = plt.subplots(1,1,figsize=(15,10))
    ax.plot(df[timeField], df[field],"ro")
    ax.plot(df[timeField], df[field])
    ax.plot(df.loc[xHi,timeField],df.loc[xHi,field],"bs",markersize=10)
    ax.plot(df.loc[xLo,timeField],df.loc[xLo,field],"gs",markersize=10)
    #hlines(y, xmin, xmax, colors='k', linestyles='solid', label='', \*, data=None, \*\*kwargs)[source]
    ax.hlines([yHi,threshHi*yHi,0.1*yHi],0,12000)
    ax.vlines(df.loc[xHi,timeField],0,1.1)
    ax.vlines(df[timeField][xLo],0,0.6)
    ax.text(df.loc[xHi,timeField]+200,yHi+.02,"100% I_ISO_RMS" )
    ax.text(df.loc[xHi,timeField]+200,threshHi*yHi +.02,f"{threshHi:.0%} I_ISO_RMS" )
    ax.text(df.loc[xHi,timeField]+200,threshLo*yHi +.02,f"{threshLo:.0%} I_ISO_RMS" )
    ax.text(df.loc[xHi,timeField]+500,np.max(df[field]),f"ISO RMS = {yHi:.3} kA",fontsize=18 )
    ax.set_xlabel("Time (uSec)")
    ax.set_ylabel("Current (kA)")
    #ax.legend(["Samples","","Final 'first point below threshold'"])
    ax.grid()
    plt.show()


# In[88]:


def plotResults_PeakCurrentMethod(df, field, timeField, peak, mssHiList, mssLoList, threshHi, threshLO, ymin, ymax):
    xHi = mssHiList[-1][0]
    yHi = np.sqrt(mssHiList[-1][1])
    xLo = mssLoList[-1][0]
    yLo = np.sqrt(mssLoList[-1][1])

    f, ax = plt.subplots(1,1,figsize=(15,10))
    ax.plot(df[timeField], df[field],"ro")
    ax.plot(df[timeField], df[field])
    ax.plot(df.loc[xHi,timeField],df.loc[xHi,field],"bs",markersize=10)
    ax.plot(df.loc[xLo,timeField],df.loc[xLo,field],"gs",markersize=10)
    #hlines(y, xmin, xmax, colors='k', linestyles='solid', label='', \*, data=None, \*\*kwargs)[source]
    ax.hlines([peak,threshHi*peak,0.1*peak],0,12000)
    ax.vlines(df.loc[xHi,timeField],0,1.1)
    ax.vlines(df[timeField][xLo],0,0.6)
    ax.text(df.loc[xHi,timeField]+200,peak+.02,"100% I_Peak" )
    ax.text(df.loc[xHi,timeField]+200,threshHi*peak +.02,f"{threshHi:.0%} I_Peak" )
    ax.text(df.loc[xHi,timeField]+200,threshLo*peak +.02,f"{threshLo:.0%} I_Peak" )
    ax.text(df.loc[xHi,timeField]+500,np.max(df[field]),f"ISO RMS = {yHi:.3} kA",fontsize=18 )
    ax.set_xlabel("Time (uSec)")
    ax.set_ylabel("Current (kA)")
    #ax.legend(["Samples","","Final 'first point below threshold'"])
    ax.grid()
    plt.show()


# In[89]:


field_mm400 = "C"
field_nrwm = "C"

timeField_mm400 = 'TIME'
timeField_nrwm = 'TIME'

threshHi = 0.9
threshLo = 0.1


# In[90]:


mssHiList, mssLoList = findEndOfWeldCandidates(df_mm400, field_mm400, threshHi, threshLo)
plotResults(df_mm400, field_mm400, timeField_mm400,  mssHiList, mssLoList, threshHi, threshLo, 0, 1.2)


# In[91]:


mssHiList, mssLoList = findEndOfWeldCandidates(df_nrwm, field_nrwm, threshHi, threshLo)
plotResults(df_nrwm, field_nrwm, timeField_nrwm, mssHiList, mssLoList, threshHi, threshLo, 0, 1.2)


# In[ ]:





# In[92]:


mssHiList, mssLoList,peak = findEndOfWeldCandidates_PeakCurrentMethod(df_mm400, field_mm400, threshHi, threshLo)
plotResults_PeakCurrentMethod(df_mm400, field_mm400, timeField_mm400, peak, mssHiList, mssLoList, threshHi, threshLo, 0, 1.2)


# In[93]:


mssHiList, mssLoList,peak = findEndOfWeldCandidates_PeakCurrentMethod(df_nrwm, field_nrwm, threshHi, threshLo)
plotResults_PeakCurrentMethod(df_nrwm, field_nrwm, timeField_nrwm, peak, mssHiList, mssLoList, threshHi, threshLo, 0, 1.2)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




