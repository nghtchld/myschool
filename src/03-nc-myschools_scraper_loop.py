#!/usr/bin/env python
# coding: utf-8

# # Loop of clean MySchool results code for scraping all results 

# In[1]:


import pandas as pd
import numpy as np
import requests
import re
import pickle
import time
import os


# In[2]:


# setting directories for file loads and saves
logs_dir = "../data/logs/"
data_dir = "../data/raw/"
load_dir = save_dir = "../data/interim/"
final_dir = "../data/processed/"


# ## load in reference data files for scraper

# In[4]:


# testing directories
all_school_years_df = pd.read_pickle(load_dir + "all_school_years_df.pickle")
all_school_years_df.head()


# ## import previously generated School IDs list
# The first school ID will be used in the URL and Request to start the loop
# * BIG TODO make DF or List of ALL schools for EACH results year! and use below
# * TODO write code for accessing latest school profile xlsx file from site and extracting just the 'ACARA School ID' values to a list / df

# In[ ]:





# ## global variables here

# In[5]:


# params for Request and vars for loops
SchoolYearId = "9"
DomainId = ["1", "2", "4", "5", "6"]
ViewModeId = "0"
years_str = ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']
years_int =  [int(y) for y in years_str]

# DomainId dict 
dict_DomainId = {
    '1' : 'Reading',
    '2' : 'Writing',
    '4' : 'Spelling',
    '5' : 'Grammar and Punctuation',
    '6' : 'Numeracy'
    }


# In[9]:



# initialise remaining schools IDs list 
# in first phase, only generate a list for one year and school type
school_type = ['Combined', 'Secondary']
               
one_year_all_schools_list = all_school_years_df.loc[
    (all_school_years_df['Calendar Year'] == years_int[-1]) & 
    (all_school_years_df['School Type'].isin(school_type)), 
                                        'ACARA School ID'].values.tolist()

remaining_schools_list = one_year_all_schools_list

# initialise DF
df_columns = ['schoolId', 'grade', 'year', 'domain', 'mean', 'lower', 'upper']
df_dtypes = {'schoolId' : int, 'grade' : int, 'year' : int, 'domain' : str,
             'mean': int, 'lower': int, 'upper': int}
results_df = pd.DataFrame(columns = df_columns)

# initialise test vars
last_school = 1
next_school = 'none'


# In[ ]:





# ### Re-initialise starting vars with mid-run values here

# In[ ]:


# Vars to change to restart scrape from middle of run
# load previously scraped results df
results_df = pd.read_csv("Courses/myschool/40151_results_df.csv")

# re-initialise test vars
last_school = 1


# In[ ]:


# load shool IDs list and pop errored 
f = open("remaining_schools_list.pickle", "rb")
remaining_schools_list = pickle.load(f)
f.close()

remaining_schools_list.pop(0)

#check test vars not equal
print('next: ',remaining_schools_list[0])
last_school = 1


# In[ ]:


last_school = 1
remaining_schools_list[:5]


# ## Loop starts here

# In[10]:


# initialise log file with run info
log = open(logs_dir + "log_myschools_runs.txt", "a+")
log.write('\r\n----New Run---- starting with next school: ' + next_school + '\r\n')
# TODO add proper logging to project and or add DateTime stamp
log.close()
    
# Outer Loop for ALL schools starts here
while len(remaining_schools_list) > 0:
    
    # check that there are still schools remaining
    if len(remaining_schools_list) == 0:
        break
        
        
    #setting a check var for infinite loop
    last_school = next_school
    
    #select the next school ID for url request
    next_school = str(remaining_schools_list[0])
    
    print('remaining schools:', len(remaining_schools_list),
     'next school:', next_school)
    
    log = open(logs_dir + "log_myschools_runs.txt", "a+")
    log.write('remaining schools: ' + str(len(remaining_schools_list)) 
              + ', next school: ' + str(next_school) + '\n')
    log.close()
    
    
    #check that we are not in a loop over the same school
    if next_school == last_school:
        #write current data sets to file and then break download loop
        results_df.to_csv(save_dir + last_school + "_results_df.csv")
        
        pickle_on = open(save_dir + "remaining_schools_list.pickle", "wb")
        pickle.dump(remaining_schools_list, pickle_on)
        pickle_on.close()
        
        f = open(logs_dir + last_school + "_error_text.html", "w+")
        f.write(text)
        f.close()
        
        break

    time.sleep(1)
    
    # Inner loop 1 for ALL years loop starts here
    #for y in range(len(years_str)):
#    for y in '0':
# CURRENTLY YEAR loop commented out for testing
    url_year = years_str[-1]        
#    time.sleep(1)
    #print('Year: ', url_year)


    # Inner loop 2 for ALL domains loop starts here 
    for d in range(len(DomainId)):
        # Loop variables here
        similar_schools_list = []
        mean_list = []
        lower_list = []
        upper_list = []

        # URL generation here
        url = ("https://www.myschool.edu.au/school/" 
               + next_school
               + "/naplan/similar/"
               + url_year)
        #print(url)

        # adding data for POST to retrieve similar school list (ViewModeId = 1)
        payload = {"SchoolYearId" : SchoolYearId, 
                   "DomainId" : DomainId[d], 
                   "ViewModeId" : ViewModeId}
        #print(payload)

        # Packages the request, send the request and catch the response: r
        r = requests.post(url, data = payload)

        # Extract the response: text
        text = r.text

        # check returned text is not an error page
        # if it is an error page then try removing that schoolID and retry
        if (len(re.findall('Server Error', text)) > 0 or
            len(re.findall('Page Not Found', text)) > 0):
            #remove errored schoolId from list, retry
            remaining_schools_list.pop(0)
            #set next_school value to foo so it doesn't break loop check
            next_school = 'foo'

            break

        else:
            # RE to scrape all the results from the request
            similar_schools_list = re.findall(r'schoolId\\":(\d*)', text)
            similar_schools_list = [int(i) for i in similar_schools_list]
            mean_list = re.findall(r'mean\\":(\d*)', text)
            mean_list = [int(i) for i in mean_list]
            lower_list = re.findall(r'lowerMargin\\":(\d*)', text)
            lower_list = [int(i) for i in lower_list]
            upper_list = re.findall(r'upperMargin\\":(\d*)', text)
            upper_list = [int(i) for i in upper_list]

            # make the df from the results
            temp_results_df = pd.DataFrame({'schoolId' : similar_schools_list, 
                                            'grade' : int(SchoolYearId), 
                                            'year' : int(url_year),
                                            'domain' : dict_DomainId[DomainId[d]],
                                            'mean' : mean_list, 
                                            'lower' : lower_list,
                                            'upper' : upper_list}
                                     ).sort_values(['schoolId'])

            results_df = results_df.append(temp_results_df, ignore_index=True)
            #print('size of results_df:', len(results_df['schoolId']))
            #print('---------\n')

        #print('\n-----------\n----------\nEnd ofallALL DOMAINS loop')
        
    # remove this group of schools from the all school ids list
    remaining_schools_list = [x for x in remaining_schools_list if x not in similar_schools_list]

        
        
    #print(remaining_schools_list[:5])
    #print('\n-------------------------------\nEnd of all YEARS loop')
    
print('----End of Scrape!----')

results_df.to_csv(final_dir + "2017_year_9_results_df.csv")


# In[ ]:


# Upon error above, save current results and sub-results by running this
results_df.to_csv(last_school + "_results_df.csv")

pickle_on = open(save_dir + "remaining_schools_list.pickle", "wb")
pickle.dump(remaining_schools_list, pickle_on)
pickle_on.close()

f = open(save_dir + last_school + "_error_text.html", "w+")
f.write(text)
f.close()


# In[ ]:


# common error: ValueError: arrays must all be same length
# check that results lists have the same length
print(len(similar_schools_list), len(mean_list), 
      len(lower_list), len(upper_list))


# In[14]:


results_df.to_csv(final_dir + "2017_year_9_results_df.csv")


# In[13]:


results_df.head()


# In[ ]:


# if you can correct results from errored run, then append df
temp_results_df = pd.DataFrame({'schoolId' : similar_schools_list, 
                                            'grade' : int(SchoolYearId), 
                                            'year' : int(url_year),
                                            'domain' : dict_DomainId[DomainId[d]],
                                            'mean' : mean_list, 
                                            'lower' : lower_list,
                                            'upper' : upper_list}
                                     ).sort_values(['schoolId'])

results_df = results_df.append(temp_results_df, ignore_index=True)


# In[ ]:





# In[15]:


results_df.tail(5)


# In[ ]:


results_df.info()


# In[ ]:


temp_results_df = pd.DataFrame({'schoolId' : '41798', 
                                'grade' : int(SchoolYearId), 
                                'year' : int(url_year),
                                'domain' : 'Numeracy',
                                'mean' : '412', 
                                'lower' : '372',
                                'upper' : '453'}, index=[42976]
                                     )

results_df = results_df.append(temp_results_df, ignore_index=True)


# In[ ]:


one_year_all_schools_df = all_school_years_df.loc[years_int[-1]]
one_year_all_schools_list = one_year_all_schools_df['ACARA School ID'].values.tolist()
remaining_schools_list = ([x for x in one_year_all_schools_list 
                           if x not in results_df['schoolId'].values.tolist()])
print(len(one_year_all_schools_list), len(remaining_schools_list))
remaining_schools_list[:10]


# In[ ]:


remaining_schools_list = [x for x in remaining_schools_list if x > 41725]
print(len(one_year_all_schools_list), len(remaining_schools_list))
remaining_schools_list[:10]


# In[ ]:


del remaining_schools_list[:8]
remaining_schools_list[:10]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




