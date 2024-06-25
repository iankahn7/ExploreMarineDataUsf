# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 13:42:34 2024

@author: ikahn




"""

import os
import scipy.io
import numpy as np
import pandas as pd
from datetime import datetime


# Load the .mat file containing time references
timeMat = scipy.io.loadmat('tchar.mat')
t_ref_char = timeMat['t_ref_char']



# Convert datetime strings to datetime objects
timeStamps = [datetime.strptime(t, '%m/%d/%Y %H:') for t in t_ref_char.flatten()]

# Load the water level data
mat = scipy.io.loadmat('noaa.mat')
noaa_raw = mat['noaa_raw']
station_names = [name[0][0] for name in mat['name']]

# Function to convert datetime object to its components
def datetime_to_vector(dt):
    return [dt.year, dt.month, dt.day, dt.hour]

# Apply the function to each datetime object in the timeStamps list
vectors = [datetime_to_vector(dt) for dt in timeStamps]

# Initialize dictionaries to store the long-term monthly averages
longterm_monthly_averages = {station_index: {month: [] for month in range(1, 13)} for station_index in range(len(station_names))}

# Loop over each station
for station_index in range(noaa_raw.shape[1]):
    # Loop over each datetime vector and corresponding water level
    for vector, water_level in zip(vectors, noaa_raw[:, station_index]):
        _, month, _, _ = vector
        
        if not np.isnan(water_level):  # Check for NaN and ignore if NaN
            longterm_monthly_averages[station_index][month].append(water_level)

# Calculate the long-term average for each month and station
longterm_average_matrix = {station_index: {month: -999 for month in range(1, 13)} for station_index in range(len(station_names))}

for station_index, months in longterm_monthly_averages.items():
    for month, values in months.items():
        if values:  # Check if there are any values
            longterm_average_matrix[station_index][month] = np.mean(values)

# Prepare data for CSV file
longterm_average_data = []

# Creating a DataFrame for the long-term averages
longterm_average_df = pd.DataFrame(columns=['Month'] + station_names)
for month in range(1, 13):
    row = [month]
    for station_index in range(len(station_names)):
        row.append(longterm_average_matrix[station_index][month])
    longterm_average_df.loc[len(longterm_average_df)] = row

# Save to CSV file
longterm_average_df.to_csv('longterm_monthly_average_water_levels.csv', index=False)

# Display some of the average data for verification if testingFlag is set to True
testingFlag = True
if testingFlag:
    print("Long-term Monthly Average Water Levels")
    print(longterm_average_df.head(12))