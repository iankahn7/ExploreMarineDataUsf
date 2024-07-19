# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 22:21:03 2024

@author: ikahn
"""
import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Load the .mat files
mat = scipy.io.loadmat('noaa.mat')
timeMat = scipy.io.loadmat('tchar.mat')

# Access the variables
lat = mat['lat']
lon = mat['lon']
name = mat['name']
noaa_raw = mat['noaa_raw']
t_ref_char = timeMat['t_ref_char']

# Create output directory for saving plots and text file
save_directory = 'C:\\Users\\ikahn\\Desktop\\unm\\IanKahn_RESUMES\\ocean_sci\\usf_making_waves\\Research\\screenshots'
save_directory_data = os.path.join(save_directory, 'outputData')
os.makedirs(save_directory_data, exist_ok=True)

def write_site_info_to_txt(filename, current_index):
    """
    Write site information to a text file with a star marker for the current index.

    Parameters:
    - filename (str): Name of the text file to write.
    - current_index (int): Index of the current site to mark with a star.
    """
    with open(filename, 'w') as f:
        for i in range(len(name)):
            grabbedName = name[i][0][0].strip()
            latitude = lat[i][0]
            longitude = lon[i][0]
            
            if i == current_index:
                f.write(f"* Site {i+1}:\n")
            else:
                f.write(f"  Site {i+1}:\n")
                
            f.write(f"    Name: {grabbedName}\n")
            f.write(f"    Latitude: {latitude:.8f}\n")
            f.write(f"    Longitude: {longitude:.8f}\n")
            f.write("--------------------\n")

# Get the total number of sites
total_sites = len(name)

# Prompt user to enter a site number
grabIndex = int(input(f"Enter a site number between 1 and {total_sites}: ")) - 1

# Write site information to text file
write_site_info_to_txt(os.path.join(save_directory_data, 'site_info.txt'), grabIndex)

# Scatter plot with all the latitude and longitude from this file
plt.figure(figsize=(10, 6))
plt.scatter(lon, lat)
plt.title('Latitude and Longitude of Tide Gauges')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Showing index number of each site
for i in range(len(name)):
    plt.text(lon[i], lat[i], str(i+1), fontsize=8)

# Highlight the current site with a star marker
plt.text(lon[grabIndex], lat[grabIndex], '*', fontsize=12, color='red', ha='center', va='center')

# Save the scatter plot as a high-resolution JPEG
plt.savefig(os.path.join(save_directory, 'latitude_longitude_tide_gauges.jpg'), dpi=300)

# Show the scatter plot
plt.show()

# Inspect the first few entries in t_ref_char
print("First few entries in t_ref_char:", t_ref_char[:5])

# Parsing the datetimes into times that Python can read and graph
timeStamps = []
for t in t_ref_char:
    try:
        timeStamps.append(datetime.strptime(t[0], '%m/%d/%Y %H:'))
    except ValueError as e:
        print(f"Error parsing date {t[0]}: {e}")
        continue

# Line plot of data at the given index
grabbedName = name[grabIndex][0][0]
strippedName = grabbedName.strip()
dataGrab = noaa_raw[:, grabIndex]

# Remove NaN values from dataGrab and corresponding timestamps
timeStamps_clean = [timeStamps[i] for i in range(len(timeStamps)) if not np.isnan(dataGrab[i])]
dataGrab_clean = dataGrab[~np.isnan(dataGrab)]

# Ensure the lengths are consistent
if len(timeStamps_clean) != len(dataGrab_clean):
    raise ValueError("Mismatch between timeStamps and dataGrab lengths after cleaning")

plt.figure(figsize=(10, 6))
plt.plot(timeStamps_clean, dataGrab_clean)
plt.title(f'Water Level at {strippedName}')
plt.xlabel('Time')
plt.ylabel('Water Level (CM)')

# Calculate monthly average overlay
months = [t.month for t in timeStamps_clean]
unique_months = sorted(set(months))
monthly_avg = [np.mean([dataGrab_clean[i] for i, m in enumerate(months) if m == month]) for month in unique_months]

# Add the monthly average overlay to the plot
plt.plot([datetime(year=1900, month=m, day=1) for m in unique_months], monthly_avg, label='Monthly Average', color='orange')

# Calculate trend overlay (simple linear trend)
z = np.polyfit([t.toordinal() for t in timeStamps_clean], dataGrab_clean, 1)
p = np.poly1d(z)
plt.plot(timeStamps_clean, p([t.toordinal() for t in timeStamps_clean]), label='Trend', color='red')

# Add legend
plt.legend()

# Show the line plot
plt.show()

def plot_data_with_date_range(start_date, end_date):
    """
    Plot the data within the specified date range.

    Parameters:
    - start_date (str): Start date in the format 'mm/dd/yyyy'.
    - end_date (str): End date in the format 'mm/dd/yyyy'.
    """
    # Convert string dates to datetime objects
    start_datetime = datetime.strptime(start_date, '%m/%d/%Y')
    end_datetime = datetime.strptime(end_date, '%m/%d/%Y')

    # Filter the timestamps and data within the specified date range
    filtered_timeStamps = []
    filtered_data = []
    for i, timestamp in enumerate(timeStamps_clean):
        if start_datetime <= timestamp <= end_datetime:
            filtered_timeStamps.append(timestamp)
            filtered_data.append(dataGrab_clean[i])
    
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_timeStamps, filtered_data)
    plt.title(f'Water Level (CM) at {strippedName} from {start_date} to {end_date}')
    plt.xlabel('Time')
    plt.ylabel('Water Level (CM)')

    # Save the line plot as a high-resolution JPEG
    plt.savefig(os.path.join(save_directory, f'data_plot_{strippedName}_{start_date}_to_{end_date}.jpg'), dpi=300)

    # Show the line plot
    plt.show()

