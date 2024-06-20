# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 12:06:41 2024

@author:  Ian Kahn

AI description of this file: 

This Python script, authored by Ian Kahn, is designed to process and analyze
time reference data stored in a MATLAB .mat file. The script loads the time
reference data from the tchar.mat file, which contains datetime strings. 
These strings are then converted into Python datetime objects using the 
datetime.strptime method. A function named datetime_to_vector is defined
to extract and return the year, month, day, and hour components from each
datetime object. The script applies this function to the list of datetime
objects to create a corresponding list of datetime vectors. Additionally, 
there is a flag (testingFlag) that, when set to True, will print these vectors
to the console for verification and debugging purposes. The script leverages
the scipy.io module for loading MATLAB files and the datetime module for datetime manipulations.  
"""

import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

testingFlag = False

def load_time_stamps(filename):
    """
    Load the .mat file containing time references and convert them to datetime objects.
    
    Parameters:
    filename (str): Path to the .mat file
    
    Returns:
    list: List of datetime objects
    """
    timeMat = scipy.io.loadmat(filename)
    t_ref_char = timeMat['t_ref_char']
    timeStamps = [datetime.strptime(t, '%m/%d/%Y %H:') for t in t_ref_char]
    return timeStamps

def datetime_to_vector(dt):
    """
    Convert datetime object to its components.
    
    Parameters:
    dt (datetime): A datetime object
    
    Returns:
    list: List containing year, month, day, and hour
    """
    return [dt.year, dt.month, dt.day, dt.hour]

def get_vectors_from_timestamps(timeStamps):
    """
    Apply datetime_to_vector to a list of datetime objects.
    
    Parameters:
    timeStamps (list): List of datetime objects
    
    Returns:
    list: List of vectors representing the datetime components
    """
    return [datetime_to_vector(dt) for dt in timeStamps]

def filter_by_criteria(vectors, start_year=None, end_year=None, months=None, days=None, start_hour=None, end_hour=None, num_vals=10):
    """
    Filter vectors by various criteria.
    
    Parameters:
    vectors (list): List of datetime vectors
    start_year (int): Start year of the range (inclusive)
    end_year (int): End year of the range (inclusive)
    months (list): List of months to filter by (1 for January, 2 for February, ..., 12 for December)
    days (list): List of days to filter by (1 to 31)
    start_hour (int): Start hour of the range (inclusive)
    end_hour (int): End hour of the range (inclusive)
    num_vals (int): Number of vectors to return
    
    Returns:
    list: Filtered list of datetime vectors
    """
    vectors_np = np.array(vectors)
    conditions = []

    if start_year is not None:
        conditions.append(vectors_np[:, 0] >= start_year)
    if end_year is not None:
        conditions.append(vectors_np[:, 0] <= end_year)
    if months is not None:
        conditions.append(np.isin(vectors_np[:, 1], months))
    if days is not None:
        conditions.append(np.isin(vectors_np[:, 2], days))
    if start_hour is not None:
        conditions.append(vectors_np[:, 3] >= start_hour)
    if end_hour is not None:
        conditions.append(vectors_np[:, 3] <= end_hour)

    if conditions:
        combined_condition = np.all(conditions, axis=0)
        filtered_indices = np.argwhere(combined_condition).flatten()
    else:
        filtered_indices = np.arange(len(vectors))

    return vectors_np[filtered_indices][:num_vals].tolist()

# If this script is run directly, display vectors for testing
if __name__ == "__main__":
    # Test the functionality with the provided file
    filename = 'tchar.mat'
    timeStamps = load_time_stamps(filename)
    vectors = get_vectors_from_timestamps(timeStamps)

    # Example usage of filters with a specified number of vectors to display
    num_vals = 10

    # Filter by year range and print the first num_vals vectors
    filtered_by_year_range = filter_by_criteria(vectors, start_year=2000, end_year=2005, num_vals=num_vals)
    print(f"Vectors filtered by year range 2000-2005:")
    for vector in filtered_by_year_range:
        print(vector)
    print()

    # Filter by specific months (e.g., January and February) and print the first num_vals vectors
    filtered_by_months = filter_by_criteria(vectors, months=[1, 2], num_vals=num_vals)
    print(f"Vectors filtered by January and February:")
    for vector in filtered_by_months:
        print(vector)
    print()

    # Filter by cutoff year (e.g., before 2010) and print the first num_vals vectors
    filtered_by_cutoff_year = filter_by_criteria(vectors, end_year=2010, num_vals=num_vals)
    print(f"Vectors filtered by cutoff year 2010:")
    for vector in filtered_by_cutoff_year:
        print(vector)
    print()

    # Filter by time range (e.g., from 8 AM to 12 PM) and print the first num_vals vectors
    filtered_by_time_range = filter_by_criteria(vectors, start_hour=8, end_hour=12, num_vals=num_vals)
    print(f"Vectors filtered by time range 8 AM to 12 PM:")
    for vector in filtered_by_time_range:
        print(vector)
    print()
