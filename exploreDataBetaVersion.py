# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:09:43 2024
@author: Ian G Kahn
"""

import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import webbrowser
import geocoder

# Load the .mat file
mat = scipy.io.loadmat('noaa.mat')
timeMat = scipy.io.loadmat('tchar.mat')

# Access the variables
lat = mat['lat']
lon = mat['lon']
name = mat['name']
noaa_raw = mat['noaa_raw']

# Create output directory for saving plots
save_directory = 'C:\\Users\\ikahn\\Desktop\\unm\\IanKahn_RESUMES\\ocean_sci\\usf_making_waves\\Research\\screenshots'
os.makedirs(save_directory, exist_ok=True)

# Scatter plot with all the latitude and longitude from this file
plt.figure(figsize=(10, 6))
plt.scatter(lon, lat)
plt.title('Latitude and Longitude of Tide Gauges')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Showing index number of which site it is:
for i in range(len(name)):
    plt.text(lon[i], lat[i], str(i+1), fontsize=8)

# Save the scatter plot as a high-resolution JPEG
plt.savefig(os.path.join(save_directory, 'latitude_longitude_tide_gauges.jpg'), dpi=300)

# Show the scatter plot
plt.show()

# "grabIndex" is the variable that holds the index from which we want to grab the data
grabIndex = 8  # aka station number

# Print the name, latitude, and longitude associated with the grabIndex
latitude = lat[grabIndex][0]
longitude = lon[grabIndex][0]
print(f"Name grabbed at index {grabIndex}:", name[grabIndex][0][0])
print(f"Latitude at index {grabIndex}:", latitude)
print(f"Longitude at index {grabIndex}:", longitude)

# Generate HTML content for Google Earth
html_content = f"""
<!DOCTYPE html>
<html>
  <head>
    <title>Google Earth Marker</title>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <style>
      /* Set the size of the map */
      #map {{
        height: 400px;  /* The height is 400 pixels */
        width: 100%;  /* The width is the width of the web page */
       }}
    </style>
  </head>
  <body>
    <h3>Google Earth Marker</h3>
    <div id="map"></div>
    <script>
      // Initialize and add the map
      function initMap() {{
        // The location of the marker
        var markerLocation = {{lat: {latitude}, lng: {longitude}}};
        // The map, centered at the marker
        var map = new google.maps.Map(
            document.getElementById('map'), {{zoom: 15, center: markerLocation}});
        // The marker, positioned at the markerLocation
        var marker = new google.maps.Marker({{
          position: markerLocation,
          map: map,
          title: 'Marker at NOAA Station'
        }});
      }}
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap"
    async defer></script>
  </body>
</html>
"""

# Save the HTML content to a file
html_filename = os.path.join(save_directory, 'google_earth_marker.html')
with open(html_filename, 'w') as f:
    f.write(html_content)

# Open the HTML file in a web browser
webbrowser.open(html_filename)
