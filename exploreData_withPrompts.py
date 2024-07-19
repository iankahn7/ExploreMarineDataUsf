import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import webbrowser
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

testFlag = 0

if testFlag == 1:
    print("t_ref_char", t_ref_char)


# Create output directory for saving plots and text file
save_directory = 'C:\\Users\\ikahn\\Desktop\\unm\\IanKahn_RESUMES\\ocean_sci\\usf_making_waves\\Research\\screenshots'
save_directory_data = 'C:\\Users\\ikahn\\Desktop\\unm\\IanKahn_RESUMES\\ocean_sci\\usf_making_waves\\Research\\screenshots\\outputData'
os.makedirs(save_directory, exist_ok=True)

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

total_sites = len(name)
grabIndex = int(input(f"Enter a site number between 1 and {total_sites}: "))

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
    plt.text(lon[i], lat[i], str(i+1), fontsize=8)

# Highlight the current site with a star marker
plt.text(lon[grabIndex], lat[grabIndex], '*', fontsize=12, color='red', ha='center', va='center')

# Save the scatter plot as a high-resolution JPEG
plt.savefig(os.path.join(save_directory, 'latitude_longitude_tide_gauges.jpg'), dpi=300)

# Show the scatter plot
plt.show()

#parsing the datetimes into times that python can read and graph


timeStamps = [datetime.strptime(t,'%m/%d/%Y %H:') for t in t_ref_char]


#todo for monday: look up analogy of date vector
# for the date time , know the year, month, day 


'*****************************************************************************'
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
    for i, timestamp in enumerate(timeStamps):
        if start_datetime <= timestamp <= end_datetime:
            filtered_timeStamps.append(timestamp)
            filtered_data.append(dataGrab[i])
    
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_timeStamps, filtered_data)
    plt.title(f'Water Level (CM) at {strippedName} from {start_date} to {end_date}')
    plt.xlabel('Time')
    plt.ylabel('Water Level (CM)')

    # Save the line plot as a high-resolution JPEG
    plt.savefig(os.path.join(save_directory, f'data_plot_{strippedName}_{start_date}_to_{end_date}.jpg'), dpi=300)

    # Show the line plot
    plt.show()

'*****************************************************************************************************************'

# to do : add monthly average overlay , add the trend overlay to figure and increase font size on the figure

# Line plot of data at the given index
grabbedName = name[grabIndex][0][0]
strippedName = grabbedName.strip()
dataGrab = noaa_raw[:, grabIndex]

plt.figure(figsize=(10, 6))
plt.plot(timeStamps,dataGrab)
plt.title(f'Water Level at {strippedName}')
plt.xlabel('Time')
plt.ylabel('Water Level (CM)')


# Show the line plot
plt.show()

# Open Google Earth in the browser with the coordinates, zoomed in closely
latitude = lat[grabIndex][0]
longitude = lon[grabIndex][0]
google_earth_url = f'https://earth.google.com/web/@{latitude},{longitude},50a,35y,0h,0t,0r'
webbrowser.open(google_earth_url)
