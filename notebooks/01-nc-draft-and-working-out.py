#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re
import xlrd
import pickle
import os
import requests
# from bs4 import BeautifulSoup
# or import bs4 as bs
# import json


# In[ ]:





# In[2]:


# setting directories for file loads and saves
logs_dir = "../data/logs/"
raw_dir = "../data/raw/"
load_dir = save_dir = "../data/interim/"
final_dir = "../data/processed/"


# In[6]:


xl = pd.read_pickle(load_dir + "school_profiles_2008_2017_df.pickle")
xl.head()


# In[4]:


xl.info()


# # MySchool website, Sherwood State School

# In[5]:


url = "https://www.myschool.edu.au/school/46461/naplan/similar/2017"

# Packages the request, send the request and catch the response: r
r = requests.get(url)

# Extract the response: text
text = r.text

# Print the html
text[:500]


# In[6]:


# using BeautifulSoup, turn html into cleaner text
soup = BeautifulSoup(text, "lxml")


# In[7]:


print(soup.prettify()[:500])


# In[8]:


# Find all 'script' tags (which define scripts): scripts
scripts = soup.find_all('script')

# Print the school data <script> to the shell
#print(scripts[6])

# Save the school data <script> to a text file


# In[9]:


# adding data for POST to retrieve different SchoolYearId, DomainId and ViewModeId
payload = {"SchoolYearId" : "5", "DomainId" : "1", "ViewModeId" : "0"}

# retrieving the above from the same page as r
r510 = requests.post(url, data = payload)

# Extract the response: text
text510 = r510.text

# using BeautifulSoup, turn html into cleaner text
soup510 = BeautifulSoup(text510, "lxml")


# In[10]:


# Find all 'script' tags (which define scripts): scripts
scripts510 = soup510.find_all('script')

# Print the head of scipts to the shell
#print(scripts510)


# In[11]:


type(scripts[6])


# In[23]:


type(scripts[6].contents[0].string)


# In[27]:


# This gives a string which is writable to file
scripts[6].string[:50]


# In[26]:


# Writing to files
f = open("sherwood310.txt", mode = "w", encoding = "utf-8")
f.write(scripts[6].string)
f.close()

f = open("sherwood510.txt", mode = "w", encoding = "utf-8")
f.write(scripts510[6].string)
f.close()


# In[16]:


scripts[6].attrs


# In[29]:


s310 = scripts[6].string
type(s310)


# In[30]:


s310slash =  re.sub(r'\\', '', s310)
s310colq = re.sub(r':"', ':', s310slash)
s310qcomma = re.sub(r'",', ',', s310colq)


# In[33]:


s310qcomma[:1000]


# In[35]:


s310up2data = re.sub(r'.*?data":', '', s310qcomma)
s310up2data[:500]


# In[74]:


s310apostro = re.sub(',"plotOptions(.*)', '', s310up2data)
s310datalist = re.sub("u0027", "'", s310apostro)
print(s310up2data[-500:])
s310datalist[-500:]


# In[ ]:


f = open('s310datalist.txt', mode = 'w', encoding = 'utf-8')
f.write(s310datalist)


# In[79]:


grade = 3
domain = 1
view = 0

year = 2017


# In[80]:


schoolIdList = re.findall('schoolId":(\d\d\d\d\d)', s310datalist)
meanList = re.findall('mean":(\d\d\d)', s310datalist)
lowerList = re.findall('lowerMargin":(\d\d\d)', s310datalist)
upperList = re.findall('upperMargin":(\d\d\d)', s310datalist)

sherwood_310_df = pd.DataFrame({'schoolId' : schoolIdList, 'grade' : grade, 
                                'year' : year, 'mean' : meanList, 'lower' : lowerList,
                               'upper' : upperList})

sherwood_310_df.head()


# In[ ]:


sherwood_310_df.to_csv('sherwood_310_df.csv')


# # Generic school, from the all school IDs list

# In[81]:


# adding data for POST to retrieve similar school list (ViewModeId = 1)
payload = {"SchoolYearId" : "5", "DomainId" : "1", "ViewModeId" : "1"}

# retrieving the above from the same page as r
r511 = requests.post(url, data = payload)

# Extract the response: text
text511 = r511.text

# using BeautifulSoup, turn html into cleaner text
soup511 = BeautifulSoup(text510, "lxml")


# In[84]:


f = open('soup511_pretty.html', mode = 'w', encoding = 'utf-8')
f.write(soup511.prettify())
f.close()


# In[103]:


scripts511 = soup511.find_all('script')
s311schoolList = scripts511[6].string


# In[113]:


scripts511[6].string[-500:]


# In[117]:


simimlar_schools_2017 = re.findall(r'schoolId\\":(\d\d\d\d\d)', scripts511[6].string)
#simimlar_schools_2017


# ## School profiles 2008 - 2017

# In[50]:


file = load_dir + "school-profile-2008-2017.xlsx"
xl = pd.read_excel(file, sheet_name="School Profile")
print(xl.dtypes)
xl.head()


# In[ ]:





# In[11]:


allSchoolIdsList = xl['ACARA School ID'].unique().tolist();


# In[ ]:


pickle_on = open("allSchoolIdsList.pickle", "wb")
pickle.dump(allSchoolIdsList, pickle_on)
pickle_on.close()


# In[14]:


xl.to_pickle("allSchoolProfiles_df.pickle")


# In[16]:


years = ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']


# In[ ]:


years_int = [int(y) for y in years]


# In[51]:


#xl_dtypes_dict = xl.dtypes.to_dict()
#xl_dtypes_dict


# In[ ]:





# In[ ]:





# In[ ]:





# In[9]:


all_schools_sort_list = ['Calendar Year', 'School Type', 'ACARA School ID']
all_school_years_df = xl.iloc[:, [0,1,8,5]].sort_values(all_schools_sort_list
                                                ).set_index('Calendar Year')

all_school_years_df.head()


# In[12]:


all_school_years_df.to_pickle(load_dir + "all_school_years_df.pickle")


# In[53]:


year_df = all_school_years_df.loc[years_int[0]]
one_yr_list = year_df['ACARA School ID'].values.tolist()
one_yr_list[:5]


# In[59]:


year_df = all_school_years_df.loc[(years_int[-1]) & (
    all_school_years_df['School Type'] == 'Primary')]
primary_2017_schoolID_list = year_df['ACARA School ID'].values.tolist()
primary_2017_schoolID_list[:5]


# In[ ]:





# In[ ]:





# In[77]:


xl.columns


# In[ ]:





# In[ ]:




