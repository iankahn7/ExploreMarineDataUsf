# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20  2024

@author:  Ian Kahn

This Python script processes and analyzes time reference data and water level data 
from MATLAB .mat files. It loads the time reference data from the tchar.mat file, 
converts them into Python datetime objects, and extracts the year components 
from each datetime object. It also loads water level data from the noaa.mat file 
and calculates the annual average water levels for each station, saving the results 
in a new matrix. The script leverages the scipy.io module for loading MATLAB files 
and the datetime module for datetime manipulations.
"""

import os
import scipy.io
import numpy as np
import pandas as pd
from datetime import datetime

print("Loading data and creating annual averages \n")
# Load the .mat file containing time references
timeMat = scipy.io.loadmat('tchar.mat')
t_ref_char = timeMat['t_ref_char']

# Convert datetime strings to datetime objects
timeStamps = [datetime.strptime(t, '%m/%d/%Y %H:') for t in t_ref_char]

# Function to extract year from datetime object
def get_year(dt):
    return dt.year

# Apply the function to extract year from each datetime object in the timeStamps list
years = [get_year(dt) for dt in timeStamps]

# Load the water level data and station names
mat = scipy.io.loadmat('noaa.mat')
noaa_raw = mat['noaa_raw']
station_names = mat['name']

# Initialize a dictionary to store the annual averages
annual_averages = {}

# Loop over each station
for station_index in range(noaa_raw.shape[1]):
    # Loop over each year and corresponding water level
    for year, water_level in zip(years, noaa_raw[:, station_index]):
        key = (year, station_index)
        
        if key not in annual_averages:
            annual_averages[key] = []
        
        # Append water level only if it's not NaN
        if not np.isnan(water_level):
            annual_averages[key].append(water_level)

# Calculate the average for each year and station, ignoring NaNs
annual_average_matrix = {}

for key, values in annual_averages.items():
    year, station_index = key
    if values:  # Ensure there's data to calculate the mean
        annual_average_matrix[key] = np.nanmean(values)  # Use nanmean to ignore NaNs

# Convert the dictionary to a structured array for saving
dtype = [('Year', 'i4'), ('AverageWaterLevel', 'f4')]
annual_average_data = np.array([(year, avg) for (year, station_index), avg in annual_average_matrix.items()], dtype=dtype)

# Convert to DataFrame and save as CSV
annual_average_df = pd.DataFrame(annual_average_data)
csv_file_path = r'C:\Users\ikahn\Desktop\unm\computationalFabrication\dataForModel\St_Petersburg_Annual_Average_Water_Levels.csv'
annual_average_df.to_csv(csv_file_path, index=False)

# Display some of the average data for verification if testingFlag is set to True
testingFlag = False
if testingFlag:
    print("Year  AverageWaterLevel")
    for row in annual_average_data[:10]:
        print(row)
