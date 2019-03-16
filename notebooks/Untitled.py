#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd

get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
plt.style.use('ggplot')


# In[5]:


# setting directories for file loads and saves

data_dir = "../data/raw/"
load_dir = save_dir = "../data/interim/"
final_dir = "../data/processed/"


# In[7]:


xl7 = pd.read_csv(final_dir + "2017_year_7_results_df.csv", index_col=0)
xl7.head()


# In[17]:


xl7['mean'].hist(by = xl7['domain'], bins = 50, figsize = (9,12))


# In[22]:


xl7.loc[xl7['domain'] == 'Reading'].describe()


# In[19]:


xl7.info()


# In[20]:


xl7.describe()


# In[ ]:




