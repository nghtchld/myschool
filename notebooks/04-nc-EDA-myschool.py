#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd

import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
sns.set(style='ticks', context='talk')


# In[39]:


import os
os.getcwd()


# In[3]:


# setting directories for file loads and saves
logs_dir = "../data/logs/"
data_dir = "../data/raw/"
load_dir = save_dir = "../data/interim/"
final_dir = "../data/processed/"


# In[ ]:





# In[ ]:





# In[127]:


# load 2017, Year 7, NAPLAN scrpaed results

xl7 = (pd.read_csv(final_dir + "2017_year_7_results_df.csv", index_col=0)
       .rename(columns=lambda x: x.replace(" ", "_"))
       .rename(columns=str.lower))
xl7.head()


# In[145]:


# load the school profiles 2008 - 2017 spreadsheet df: xl
file = "school_profiles_2008_2017_df.pickle"

xl = pd.read_pickle(data_dir + file)

xl.head()


# In[146]:


xl.info()


# In[5]:


#xl7['mean'].hist(by = xl7['domain'], bins = 50, figsize = (9,12))


# In[32]:


xl7.info()


# In[22]:


xl7.loc[xl7['domain'] == 'Reading'].describe()


# In[7]:


xl7.groupby(['domain']).mean().round(decimals=2)


# In[120]:


xl7.loc[xl7['schoolId'] == 41811]


# In[109]:


# find a particular ACARA school ID, e.g. Corinda State High School = 47449
# Indooroopilly State High School = 47431
# ""Brisbane Boys' College = 48011
name_of_school = "James Ruse Agricultural High School"
yr = 2017

id_of_school = (school_profiles_all.loc[
    (school_profiles_all['School Name'] == name_of_school) & 
    (school_profiles_all['Calendar Year'] == yr)]
                ['ACARA School ID']
                .values[0])

id_of_school


# In[61]:


# get index of school ID in all 2017 results list 
school_all_results_index = xl7.loc[xl7['schoolId'] == id_of_school].index.tolist()


# In[107]:


z = xl7.set_index('schoolId').loc[:, ['domain', 'mean']].groupby(['domain']).rank(method='max', ascending=False)
#len(z)
print('Max of rank:', max(z['mean']), '\nMin of rank', min(z['mean']))


# In[110]:


top_10 = z.sort_values('mean').head(5).index.tolist()
for e in top_10:
    sname = (school_profiles_all.loc[
    (school_profiles_all['ACARA School ID'] == e) & 
    (school_profiles_all['Calendar Year'] == 2017)]
                ['School Name']
                .values[0])
    print(sname,)


# In[101]:


print('Corinda rankings out of', max(z['mean']))
z.loc[47449]


# In[102]:


print('Indooroopilly rankings out of', max(z['mean']))
z.loc[47431]


# In[105]:


print('BBC rankings out of', max(z['mean']))
z.loc[48011]


# In[111]:


print('James Ruse rankings out of', max(z['mean']))
z.loc[41811]


# In[ ]:




