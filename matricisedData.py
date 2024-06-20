# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:46:58 2024
@author: ikahn
"""

import scipy.io
import numpy as np
from datetime import datetime

# Function to load time stamps from a .mat file
def load_time_stamps(filename):
    timeMat = scipy.io.loadmat(filename)
    t_ref_char = timeMat['t_ref_char']
    time_stamps = [datetime.strptime(t, '%m/%d/%Y %H:') for t in t_ref_char.flatten()]
    return time_stamps

# Function to load station metadata (names, latitude, longitude)
def load_station_metadata(filename):
    mat = scipy.io.loadmat(filename)
    names = mat['name'].flatten()
    latitude = mat['lat'].flatten()
    longitude = mat['lon'].flatten()
    return names, latitude, longitude

# Function to create a new matrix and a new time vector for the 15th of each month
def create_new_data(time_stamps, names, latitude, longitude):
    new_time_stamps = []
    new_matrix = []

    for ts in time_stamps:
        if ts.day == 15:
            new_time_stamps.append(ts)
            # Load actual data for each station (replace with actual data loading logic)
            station_data = np.random.rand(len(names)) * 10  # Example: random data; replace this with actual data loading
            new_matrix.append(station_data)

    return np.array(new_time_stamps), np.array(new_matrix)

# Metadata
metadata = {
    'created_by': 'Ian Kahn'  # Replace with actual creator information
}

# Example usage:
if __name__ == "__main__":
    # Load time stamps from tchar.mat file
    filename_time_stamps = 'tchar.mat'
    time_stamps = load_time_stamps(filename_time_stamps)
    
    # Load station metadata from another file (e.g., noaa.mat)
    filename_metadata = 'noaa.mat'
    names, latitude, longitude = load_station_metadata(filename_metadata)
    
    # Create new matrix and time vector for the 15th of each month
    new_time_stamps, new_matrix = create_new_data(time_stamps, names, latitude, longitude)
    
    # Save the new data along with metadata
    np.savez('new_data.npz', time_stamps=new_time_stamps, data=new_matrix, names=names, latitude=latitude, longitude=longitude, **metadata)

    # Print some information for verification
    print(f"New Time Stamps: {new_time_stamps}")
    print(f"New Data Matrix: {new_matrix}")
    print(f"Names: {names}")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
    print(f"Metadata: {metadata}")
