#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import pickle
import os

#import xlrd
#import requests


# In[1]:


# setting directories for file loads and saves

data_dir = "../data/raw/"
load_dir = save_dir = "../data/interim/"
final_dir = "../data/processed/"


# In[ ]:


# load the school profiles 2008 - 2017 spreadsheet as df: xl

file = data_dir + "school-profile-2008-2017.xlsx"
xl = pd.read_excel(file, sheet_name="School Profile")

# save df 
xl.to_pickle(data_dir + "school_profiles_2008_2017_df.pickle")


# In[ ]:


# generate a df for use in scrpaing loop: all_schools_sort_list

all_schools_sort_list = ['Calendar Year', 'School Type', 'ACARA School ID']
all_school_years_df = xl.iloc[:, [0,1,8,5]].sort_values(all_schools_sort_list
                                                ).set_index('Calendar Year')

all_school_years_df.to_pickle(save_dir + "all_school_years_df.pickle")

all_school_years_df.head()


# In[ ]:


# generate a list of school IDs for one year and school type

year_type_df = all_school_years_df.loc[(years_int[-1]) & (
    all_school_years_df['School Type'] == 'Primary')]

primary_2017_schoolID_list = year_df['ACARA School ID'].values.tolist()
primary_2017_schoolID_list[:5]


# In[ ]:




