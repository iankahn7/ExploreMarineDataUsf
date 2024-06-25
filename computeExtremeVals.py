# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 13:42:34 2024

@author: ikahn


computes extreme valuess

"""

import os
import scipy.io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import zscore

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

# Initialize dictionaries to store the long-term monthly averages and standard deviations
longterm_monthly_data = {station_index: {month: [] for month in range(1, 13)} for station_index in range(len(station_names))}

# Loop over each station
for station_index in range(noaa_raw.shape[1]):
    # Loop over each datetime vector and corresponding water level
    for vector, water_level in zip(vectors, noaa_raw[:, station_index]):
        _, month, _, _ = vector
        
        if not np.isnan(water_level):  # Check for NaN and ignore if NaN
            longterm_monthly_data[station_index][month].append(water_level)

# Calculate the long-term average and standard deviation for each month and station
longterm_average_matrix = {station_index: {month: -999 for month in range(1, 13)} for station_index in range(len(station_names))}
longterm_std_matrix = {station_index: {month: -999 for month in range(1, 13)} for station_index in range(len(station_names))}

for station_index, months in longterm_monthly_data.items():
    for month, values in months.items():
        if values:  # Check if there are any values
            longterm_average_matrix[station_index][month] = np.mean(values)
            longterm_std_matrix[station_index][month] = np.std(values)

# Function to identify extreme values
def identify_anomalies(data, mean, std_dev, threshold=2):
    if std_dev == 0:  # To avoid division by zero
        return np.zeros_like(data, dtype=bool)
    z_scores = (data - mean) / std_dev
    return np.abs(z_scores) > threshold


"""
we have the monthly averages, and the climatological average,

monthly Anomaly = monthly averages - climatological

create new csv file

"""

# Prepare data for anomalies
anomalies = []

# Loop over each station
for station_index in range(noaa_raw.shape[1]):
    # Loop over each datetime vector and corresponding water level
    for vector, water_level in zip(vectors, noaa_raw[:, station_index]):
        year, month, day, hour = vector
        if not np.isnan(water_level):  # Check for NaN and ignore if NaN
            mean = longterm_average_matrix[station_index][month]
            std_dev = longterm_std_matrix[station_index][month]
            if identify_anomalies(water_level, mean, std_dev):
                anomalies.append([year, month, day, hour, station_index, water_level, mean, std_dev])

# Convert anomalies to DataFrame
anomalies_df = pd.DataFrame(anomalies, columns=['Year', 'Month', 'Day', 'Hour', 'StationIndex', 'WaterLevel', 'Mean', 'StdDev'])

# Save to CSV file
anomalies_df.to_csv('anomalies.csv', index=False)

# Prepare data for CSV file of long-term monthly averages
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

# Helper function to plot anomalies for a given station index
def plot_anomalies(station_index):
    station_anomalies = anomalies_df[anomalies_df['StationIndex'] == station_index]
    
    if station_anomalies.empty:
        print(f"No anomalies found for station index {station_index}.")
        return
    
    plt.figure(figsize=(12, 6))
    plt.plot(station_anomalies['Year'], station_anomalies['WaterLevel'], 'ro', label='Anomalies')
    plt.axhline(y=0, color='gray', linestyle='--')
    plt.xlabel('Year')
    plt.ylabel('Water Level')
    plt.title(f'Anomalies in Water Levels for Station Index {station_index} ({station_names[station_index]})')
    plt.legend()
    plt.show()

# Example usage of plot_anomalies function
plot_anomalies(0)  # Replace 0 with the actual station index you want to plot

# Display some of the average data for verification if testingFlag is set to True
testingFlag = True
if testingFlag:
    print("Long-term Monthly Average Water Levels")
    print(longterm_average_df.head(12))
    print("Anomalies")
    print(anomalies_df.head(10))
