#!/usr/bin/env python
# coding: utf-8

# # Loop of clean MySchool results code for scraping all results 

# In[1]:


import pandas as pd
import numpy as np
import requests
import re
import pickle


# ## import previously generated School IDs list
# The first school ID will be used in the URL and Request to start the loop
# * TODO write code for accessing latest school profile xlsx file from site and extracting just the 'ACARA School ID' values to a list / df

# In[3]:


pickle_off = open("allSchoolIdsList.pickle", "rb")
all_school_ids_list = pickle.load(pickle_off)
pickle_off.close()
all_school_ids_list[:5]


# ## global variables here

# In[17]:


SchoolYearId = "5"
DomainId = ["1", "2", "4", "5", "6"]
ViewModeId = "0"
year = ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']


# ## Loop starts here

# In[21]:


url = ("https://www.myschool.edu.au/school/" 
       + str(all_school_ids_list[0])
       + "/naplan/similar/"
       + year[-1])
print(url)

# adding data for POST to retrieve similar school list (ViewModeId = 1)
payload = {"SchoolYearId" : SchoolYearId, "DomainId" : DomainId[0], "ViewModeId" : ViewModeId}
print(payload)


# In[15]:


# Packages the request, send the request and catch the response: r
r = requests.get(url, data = payload))

# Extract the response: text
text = r.text

text[:50]


# In[16]:


f = open('test_text.html', mode = 'w', encoding = 'utf-8')
f.write(text)
f.close()


# In[25]:


similar_schools = re.findall(r'schoolId\\":(\d\d\d\d\d)', text)
similar_schools = [int(i) for i in similar_schools]
similar_schools[:5]


# In[ ]:





# In[ ]:




