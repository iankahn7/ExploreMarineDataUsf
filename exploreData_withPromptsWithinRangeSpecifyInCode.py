import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Load the .mat file
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
os.makedirs(save_directory, exist_ok=True)
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

def filter_data_by_month_range(start_date, end_date, target_month):
    """
    Filter data for a specific month within the specified date range.

    Parameters:
    - start_date (str): Start date in the format 'mm/dd/yyyy'.
    - end_date (str): End date in the format 'mm/dd/yyyy'.
    - target_month (int): Month number (1-12) to filter data for.
    """
    # Convert string dates to datetime objects
    start_datetime = datetime.strptime(start_date, '%m/%d/%Y')
    end_datetime = datetime.strptime(end_date, '%m/%d/%Y')

    # Filter the timestamps and data for the specified month within the date range
    filtered_timeStamps = []
    filtered_data = []
    for i, timestamp in enumerate(timeStamps):
        if start_datetime <= timestamp <= end_datetime and timestamp.month == target_month:
            filtered_timeStamps.append(timestamp)
            filtered_data.append(dataGrab[i])
    
    return filtered_timeStamps, filtered_data

# Parsing the datetimes into times that Python can read and graph
"*********************************************************************"
timeStamps = [datetime.strptime(t,'%m/%d/%Y %H:') for t in t_ref_char]
"*********************************************************************"

# Prompt user input for site selection
total_sites = len(name)
grabIndex = int(input(f"Enter a site number between 1 and {total_sites}: ")) - 1

# Write site information to text file
write_site_info_to_txt(os.path.join(save_directory_data, 'site_info.txt'), grabIndex)

# Scatter plot with all the latitude and longitude from this file
plt.figure(figsize=(10, 6))
plt.scatter(lon, lat)
plt.title('Latitude and Longitude of Tide Gauges')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Showing index number of which site it is:
for i in range(len(name)):
    plt.text(lon[i][0], lat[i][0], str(i+1), fontsize=8)

# Highlight the current site with a star marker
plt.text(lon[grabIndex][0], lat[grabIndex][0], '*', fontsize=12, color='red', ha='center', va='center')

# Save the scatter plot as a high-resolution JPEG
plt.savefig(os.path.join(save_directory, 'latitude_longitude_tide_gauges.jpg'), dpi=300)

# Show the scatter plot
plt.show()

# Line plot of data at the given index
grabbedName = name[grabIndex][0][0]
strippedName = grabbedName.strip()
dataGrab = noaa_raw[:, grabIndex]

# Function to plot data for specific months within a date range
def plot_data_for_specific_months(start_date, end_date, target_month):
    """
    Plot data for specific months within the date range.

    Parameters:
    - start_date (str): Start date in the format 'mm/dd/yyyy'.
    - end_date (str): End date in the format 'mm/dd/yyyy'.
    - target_month (int or list of ints): Month(s) to plot data for.
    """
    if isinstance(target_month, int):
        target_month = [target_month]

    # Plot data for each specified month
    for month in target_month:
        filtered_timeStamps, filtered_data = filter_data_by_month_range(start_date, end_date, month)

        plt.figure(figsize=(10, 6))
        plt.plot(filtered_timeStamps, filtered_data)
        plt.title(f'Plot of Water Level (CM) at {strippedName} for Month {month} from {start_date} to {end_date}')
        plt.xlabel('Time')
        plt.ylabel('Water Level (CM)')

        # Save the line plot as a high-resolution JPEG
        plt.savefig(os.path.join(save_directory, f'data_plot_{strippedName}_month_{month}_{start_date}_to_{end_date}.jpg'), dpi=300)

        # Show the line plot
        plt.show()

# Example usage: Plot data for all Februarys within a specific date range

"modify below:"
"****************************************************************************"
start_date = '01/01/2000'
end_date = '12/31/2005'
target_month = 2  # February
"****************************************************************************"

plot_data_for_specific_months(start_date, end_date, target_month)

