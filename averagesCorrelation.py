# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:06:58 2024

@author: Ian Kahn


contains helper function that plots the correlation between the average monthly 
water levels of two specified stations. This will help visualize the 
relationship between the water levels recorded at different stations.


Positive Correlation: If the points tend to lie along a line that slopes upward from left to right, it indicates a positive correlation. This means that when the average water level at the first station increases, the average water level at the second station also tends to increase.
Negative Correlation: If the points tend to lie along a line that slopes downward from left to right, it indicates a negative correlation. This means that when the average water level at the first station increases, the average water level at the second station tends to decrease.
No Correlation: If the points are widely scattered with no discernible pattern, it indicates little to no correlation between the water levels at the two stations.
"""


import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


# Load the .mat file containing time references
timeMat = scipy.io.loadmat('tchar.mat')
t_ref_char = timeMat['t_ref_char']

# Convert datetime strings to datetime objects
timeStamps = [datetime.strptime(t, '%m/%d/%Y %H:') for t in t_ref_char]

# Load the water level data
mat = scipy.io.loadmat('noaa.mat')
noaa_raw = mat['noaa_raw']
station_names = mat['name']

# Function to convert datetime object to its components
def datetime_to_vector(dt):
    return [dt.year, dt.month, dt.day, dt.hour]

# Apply the function to each datetime object in the timeStamps list
vectors = [datetime_to_vector(dt) for dt in timeStamps]

# Initialize a dictionary to store the monthly averages
monthly_averages = {}

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

# Calculate the average for each month and station
average_matrix = {}

for key, values in monthly_averages.items():
    year, month, station_index = key
    average_matrix[key] = np.mean(values)

# Convert the dictionary to a structured array for saving
dtype = [('Year', 'i4'), ('Month', 'i4'), ('StationIndex', 'i4'), ('AverageWaterLevel', 'f4')]
average_data = np.array([(year, month, station_index, avg) for (year, month, station_index), avg in average_matrix.items()], dtype=dtype)

# Save the structured array to a .npz file
np.savez('monthly_average_water_levels.npz', average_data=average_data)

# Display some of the average data for verification if testingFlag is set to True
testingFlag = False
if testingFlag:
    print("Year  Month  StationIndex  AverageWaterLevel")
    for row in average_data[:10]:
        print(row)



# Helper function to plot correlation between two stations
def plot_correlation(station_index1, station_index2):
    # Filter data for the specified stations
    filtered_data1 = average_data[average_data['StationIndex'] == station_index1]
    filtered_data2 = average_data[average_data['StationIndex'] == station_index2]
    
    # Find common dates
    common_dates = set((row['Year'], row['Month']) for row in filtered_data1).intersection(
                   set((row['Year'], row['Month']) for row in filtered_data2))
    
    # Prepare data for plotting
    data1 = []
    data2 = []
    
    for year, month in common_dates:
        avg_level1 = filtered_data1[(filtered_data1['Year'] == year) & (filtered_data1['Month'] == month)]['AverageWaterLevel']
        avg_level2 = filtered_data2[(filtered_data2['Year'] == year) & (filtered_data2['Month'] == month)]['AverageWaterLevel']
        if avg_level1.size > 0 and avg_level2.size > 0:
            data1.append(avg_level1[0])
            data2.append(avg_level2[0])
    
    # Retrieve the station names
    station_name1 = station_names[station_index1][0][0]
    station_name2 = station_names[station_index2][0][0]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(data1, data2)
    plt.title(f'Correlation between {station_name1} and {station_name2} Monthly Averages')
    plt.xlabel(station_name1)
    plt.ylabel(station_name2)
    plt.grid(True)
    plt.show()

# Plot correlation between two stations

"station_index == site number "
station_index1 =  0  # Change this to the first station index
station_index2 = 17 # Change this to the second station index



plot_correlation(station_index1, station_index2)

