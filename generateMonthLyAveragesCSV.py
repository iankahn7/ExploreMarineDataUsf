"""
Author: Ian Kahn

Put the monthly averages into a matrix, one station at a time, then print that
to the CSV file
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

# Initialize dictionaries to store the monthly averages and count of good points
monthly_averages = {}
monthly_good_points = {}

# Loop over each station
for station_index in range(noaa_raw.shape[1]):
    # Loop over each datetime vector and corresponding water level
    for vector, water_level in zip(vectors, noaa_raw[:, station_index]):
        year, month, _, _ = vector
        key = (year, month, station_index)
        
        if key not in monthly_averages:
            monthly_averages[key] = []
        
        if not np.isnan(water_level):  # Check for NaN and ignore if NaN
            monthly_averages[key].append(water_level)

# Calculate the average and count for each month and station
average_matrix = {}
good_points_matrix = {}

for key, values in monthly_averages.items():
    year, month, station_index = key
    average_matrix[key] = np.mean(values)
    good_points_matrix[key] = len(values)

# Creating a sorted list of all unique (year, month) pairs
dates = sorted(set((key[0], key[1]) for key in average_matrix.keys()))

# Prepare data for CSV files
average_data = []
good_points_data = []

# Adding "Year" and "Month" headers to the data
average_data.append(["Year", "Month"] + station_names)
good_points_data.append(["Year", "Month"] + station_names)

# Populate the dataframes with the calculated values
for (year, month) in dates:
    average_row = [year, month]
    good_points_row = [year, month]
    for station_index in range(len(station_names)):
        average_row.append(average_matrix.get((year, month, station_index), np.nan))
        good_points_row.append(good_points_matrix.get((year, month, station_index), np.nan))
    average_data.append(average_row)
    good_points_data.append(good_points_row)

# Convert to DataFrame
average_df = pd.DataFrame(average_data[1:], columns=average_data[0])
good_points_df = pd.DataFrame(good_points_data[1:], columns=good_points_data[0])

# Save to CSV files
average_df.to_csv('monthly_average_water_levels.csv', index=False)
good_points_df.to_csv('monthly_good_points_count.csv', index=False)

# Display some of the average data for verification if testingFlag is set to True
testingFlag = True
if testingFlag:
    print("Monthly Average Water Levels")
    print(average_df.head(10))
    print("Monthly Good Points Count")
    print(good_points_df.head(10))
