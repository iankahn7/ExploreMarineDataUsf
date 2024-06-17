# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 08:51:45 2024

@author: ikahn
"""

import scipy.io
import matplotlib.pyplot as plt
import numpy as np

"bool for printing out verbosely for testing, 0 for false, 1 for true"
testFlag = 1
# Load the .mat file
mat = scipy.io.loadmat('noaa.mat')

timeMat = scipy.io.loadmat('tchar.mat')

if testFlag == 1:
    print(timeMat)
    print("\n")
    print("\n")
    print("\n")
    print(" time mat keys: \n")
    print(timeMat.keys())
    "to see what variables are in here"

# Access the variables
lat = mat['lat']
lon = mat['lon']
name = mat['name']
noaa_raw = mat['noaa_raw']

t_ref_char = timeMat['t_ref_char']
print("\n")
print("Dimensions of noaa_raw:", noaa_raw.shape)
print("output is in format (rows, columns)")
print("\n")
# Print the variables to verify they have been loaded correctly
print("lat:", lat)
print("lon:", lon)
print("name:", name)
print("noaa_raw:", noaa_raw)
print("t_ref_char", t_ref_char)

# Convert t_ref_char to datetime
t_ref_char_str = [str(i[0]).strip()[:-1] + '00' for i in t_ref_char]  # remove trailing colon and add '00' for seconds
t_ref_char_dt = []
for i in t_ref_char_str:
    try:
        t_ref_char_dt.append(np.datetime64(i, 'm'))
    except ValueError as e:
        print(f"Error converting {i} to datetime64: {e}")
        t_ref_char_dt.append(np.datetime64('NaT'))

if testFlag == 1:
    print("\nConverted datetime values (first 10):\n", t_ref_char_dt[:10])  # print first 10 for verification

# Make scatter plot with all the latitude and longitude from this file
plt.scatter(lon, lat)
plt.title('Latitude and Longitude of Tide Gauges')
plt.xlabel('Longitude ')
plt.ylabel('Latitude ')

"grabIndex is the variable that holds the index in which we want to grab the data"
grabIndex = 15
"**************************************"
grabbedName = name[grabIndex]
strippedName = grabbedName[0]
fullyStrippedName = strippedName[0]
print(f"Name grabbed at index {grabIndex}:", fullyStrippedName)

"data grab is the variable that holds the data at a given index"
dataGrab = noaa_raw[:, grabIndex]
print(f"Data grabbed at index {grabIndex} in noaa_raw:", noaa_raw[:, grabIndex])

# Filter out NaT values from t_ref_char_dt and corresponding dataGrab values
valid_indices = [i for i in range(len(t_ref_char_dt)) if t_ref_char_dt[i] != np.datetime64('NaT')]
t_ref_char_dt = [t_ref_char_dt[i] for i in valid_indices]
dataGrab = [dataGrab[i] for i in valid_indices]

if testFlag == 1:
    print("\nFiltered datetime values (first 10):\n", t_ref_char_dt[:10])
    print("\nFiltered data values (first 10):\n", dataGrab[:10])

# Ensure t_ref_char_dt and dataGrab have the same length
if len(t_ref_char_dt) != len(dataGrab):
    print("Warning: Lengths of t_ref_char_dt and dataGrab do not match!")
else:
    # Convert dataGrab to a numpy array to ensure compatibility with matplotlib
    dataGrab = np.array(dataGrab, dtype=np.float64)
    
    plt.figure(2)
    plt.plot(t_ref_char_dt, dataGrab)
    plt.title(f'Plot of Data at {fullyStrippedName} in noaa_raw data set')
    plt.xlabel('Time')
    plt.ylabel('Value')

    plt.show()