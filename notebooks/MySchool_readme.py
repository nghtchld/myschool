#!/usr/bin/env python
# coding: utf-8

# # MySchool data scraping project

# ## Done
# * Done the basic data scraping from a base school starting page.
# * Done the basic POST Request to get other grade, domain and viewMode from base page
# * Done write dictionaries for year, grade, domain and viewMode
# * Done worked out how to change year of data, adding year to end of URL
# * DONE dl schools list file and import lists / df of name and Id
# * NOT NEEDED instead generate schoolsId list from first results page (was * RE pattern needed to scrape school group list from that view)
# * Mostly DONE loop using the Loop Structure plan below for cycling through the school groups
# * Basic Version DONE loop for removing the collected schoolIds / rows from the total list / df
# 
# ## BIG TODO
# * write better school ID list generator for primary, high and special school data separation
# * reset CWD to P:etc and update file lists between H:etc and P:etc
# * set up proper directory structure in folder for project
# * git this project
# * write function defs for cleaning etc
# * write classes for the functions
# * do EDA and subsequent Analysis and Visualisations
# 
# ## Biggest TODO
# * github and docker and setup project
# * turn all data into various df, DB, linked table objects
# * make visualisations interactive / animated
# * make visualisations website
# * write unit-tests, exception catching, error raising etc
# 

# # Loop structure

# * set up vars, lists, dicts for generating Requests 
# 
# * check there are remaining schools
# * starting with the first schools ID on the all schools  list / df 
# * Request the school list View for the group of similar schools
# * initiate storage lists and DF using schools list group data
# * Request the base data page View (Year 3, Reading, 2017)
# * Request data, clean and extract, listify, make temp df and Append final DF
# * loop data requests through:
#     * domains, then years, then Year 5 domains, then years
#     * reuse storage lists and temp df, Append final DF
# * remove the schools in this group from the all schools list / df
# * restart the loop with the next schoolId, if any remaining

# ## Global Vars, Dictionaries and Lists of POST data

# In[2]:


# Global variables here
# DF of ALL schools EACH year
all_school_years_df = pd.read_pickle("all_school_years_df.pickle")

# params for Request and vars for loops
SchoolYearId = "5"
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

# initialise remaining schools IDs list
one_year_all_schools_df = all_school_years_df.loc[years_int[-1]]
one_year_all_schools_list = one_year_all_schools_df['ACARA School ID'].values.tolist()
remaining_schools_list = one_year_all_schools_list

# initialise DF
df_columns = ['schoolId', 'grade', 'year', 'domain', 'mean', 'lower', 'upper']
results_df = pd.DataFrame(columns = df_columns)

# initialise test vars
last_school = 1


# In[ ]:





# In[ ]:




