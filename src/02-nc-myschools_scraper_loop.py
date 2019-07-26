#!/usr/bin/env python
# coding: utf-8
# # loop over MySchool result pages and scrape data

import pandas as pd
import numpy as np
import requests
import re
import pickle
import time
import os

# params for Request and vars for loops
# TODO need to write logic for selecting 'primary' vs 'secondary'
# TODO from df depending on value of SchoolYearId, start of list loop
# only doing 2015 to 2017 to test loop, full years list below
years_str = ['2015', '2016', '2017']
#years_str = ['2008', '2009', '2010', '2011', '2012', '2013',
#             '2014', '2015', '2016', '2017']
years_int = [int(y) for y in years_str]
grade_id = ['5', '7']
grade_id_dict = {'3': 'primary', '5': 'primary',
                 '7': 'secondary', '9': 'secondary'}
#grade_id = ['3', '5', '7', '9']
domain_id = ['1', '2', '4', '5', '6']
view_mode_id = '0'

# domain_id dictionary
domain_id_dict = {
    '1': 'Reading',
    '2': 'Writing',
    '4': 'Spelling',
    '5': 'Grammar and Punctuation',
    '6': 'Numeracy'
    }

# setting directories for file loads and saves
proc_dir = './data/processed/'
save_dir = './data/interim/'
raw_dir =  './data/raw/'
logs_dir = './data/logs/'

# Create directory to hold downloaded data
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# import previously generated profile df for all schools, years
all_schools_years_df = pd.read_pickle(proc_dir + "all_schools_years_df.pickle")


# ## import previously generated School IDs list
# The first school ID will be used in the URL and Request to start the loop
# * BIG TODO make DF or List of ALL schools for EACH results year! and use below
# * TODO write code for accessing latest school profile xlsx file from site and extracting just the 'ACARA School ID' values to a list / df


# initialise NAPLAN results DF
df_columns = ['schoolId', 'grade', 'year', 'domain', 'mean', 'lower', 'upper']
results_df = pd.DataFrame(columns=df_columns)

# initialise similar schools lists
sim_schools_all = []

# initialise test vars
next_school = str(remaining_schools_list[0])
last_school = 1

# ## Loop starts here
# initialise log file with run info
log = open(logs_dir + "log_myschools_runs.txt", "a+")
log.write('\r\n----New Run---- starting with next school: ' + next_school + '\r\n')
# TODO add proper logging to project and or add DateTime stamp
# https://www.datadoghq.com/blog/python-logging-best-practices/
log.close()

# initialise one year/grade and remaining schools IDs list
one_yr = all_school_years_df.loc[[years_int[-1]] &
                         (all_school_years_df['School Type'] == 'Primary'),
                        'ACARA School ID'].values
remaining_schools_list = one_yr

# initialise log file with grade info
log = open(logs_dir + "log_myschools_runs.txt", "a+")
log.write('\r\n----New Grade---- starting with next school: ' + next_school + '\r\n')
# TODO add proper logging to project and or add DateTime stamp
# https://www.datadoghq.com/blog/python-logging-best-practices/
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

    log = open(logs_dir + "log_myschools_runs.txt", "a+")
    log.write('remaining schools: ' + str(len(remaining_schools_list))
              + ', next school: ' + str(next_school) + '\n')
    log.close()

    #check that we are not in a loop over the same school
    if next_school == last_school:
        #write current data sets to file and then break download loop
        results_df.to_csv(last_school + "_results_df.csv")

        pickle_on = open("remaining_schools_list.pickle", "wb")
        pickle.dump(remaining_schools_list, pickle_on)
        pickle_on.close()

        f = open(last_school + "_error_text.html", "w+")
        f.write(text)
        f.close()

        break

    time.sleep(0.2)

    # Inner loop 1 for ALL years loop starts here
    for y in range(len(years_str)):
        url_year = years_str[-1]

        # Inner loop 2 for ALL domains loop starts here
        for d in range(len(domain_id)):
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
            payload = {"SchoolYearId" : grade_id,
                    "DomainId" : domain_id[d],
                    "ViewModeId" : view_mode_id}
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
                # similar schools lists collection
                sim_schools_all = sim_schools_all.append(similar_schools_list)
                mean_list = re.findall(r'mean\\":(\d*)', text)
                mean_list = [int(i) for i in mean_list]
                lower_list = re.findall(r'lowerMargin\\":(\d*)', text)
                lower_list = [int(i) for i in lower_list]
                upper_list = re.findall(r'upperMargin\\":(\d*)', text)
                upper_list = [int(i) for i in upper_list]

                # make the df from the results
                temp_results_df = pd.DataFrame({'schoolId' : similar_schools_list,
                                                'grade' : int(grade_id),
                                                'year' : int(url_year),
                                                'domain' : domain_id_dict[domain_id[d]],
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


# Upon error above, save current results and sub-results by running this
results_df.to_csv("2015_to_2018_results_df.csv")

pickle_on = open("2015_to_2018_results_df.pickle", "wb")
pickle.dump(result_df, pickle_on)
pickle_on.close()
