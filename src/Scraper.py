# loop over MySchool result pages and scrape data
import pandas as pd
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
all_schools_years_df = pd.read_pickle(proc_dir + 'all_schools_years_df.pickle')

