#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import pickle
import os

#import xlrd
#import requests


# In[10]:


# setting directories for file loads and saves
logs_dir = "../data/logs/"
raw_dir = "../data/raw/"
load_dir = save_dir = "../data/interim/"
final_dir = "../data/processed/"


# In[16]:


# load and process the school profiles 2008 - 2017 spreadsheet as df: xl

file = raw_dir + "school-profile-2008-2017.xlsx"

cols_drop =  ['AGE ID', 'Campus Type',
       'Rolled Reporting Description', 'School URL', 'Year Range',
       'Geolocation', 'Teaching Staff', 'Non-Teaching Staff', 
        'Full Time Equivalent Enrolments']

xl = (pd.read_excel(file, sheet_name="School Profile")
     .drop(labels=cols_drop, axis=1)
      .rename(columns=lambda x: x.replace(" ", "_"))
      .rename(columns=str.lower)
      .rename(mapper = {"acara_school_id" : "school_id",
                        "full_time_equivalent_teaching_staff" : "fte_teachers", 
                        "language_background_other_than_english" : "lote", 
                        "full_time_equivalent_non-teaching_staff" : "fte_other_staff", 
                        "full_time_equivalent_enrolments" : "fte_enrolments"}, axis=1)
     )

# save df 
xl.to_pickle(save_dir + "school_profiles_2008_2017_df.pickle")

xl.head()


# In[18]:


# functions to generate a school list for a grade, calendar year and school type


# In[ ]:


xl.fillna()


# In[6]:


# generate a df for use in scraping loop: all_schools_sort_list

all_schools_sort_list = ['calendar_year', 'school_type', 'ACARA School ID']
all_school_years_df = xl.iloc[:, [0,1,8,5]].sort_values(all_schools_sort_list)
all_school_years_df.reset_index(drop=True, inplace=True)

all_school_years_df.to_pickle(save_dir + "all_school_years_df.pickle")

all_school_years_df.fillna()


# In[ ]:





# In[ ]:


# generate a list of school IDs for one year and school type
school_type = ['Combined', 'Secondary']

one_year_all_schools_list = all_school_years_df.loc[
    (all_school_years_df['Calendar Year'] == years_int[-1]) & 
    (all_school_years_df['School Type'].isin(school_type)), 
                                    'ACARA School ID'].values.tolist()

primary_2017_schoolID_list[:5]


# In[ ]:





# In[ ]:




