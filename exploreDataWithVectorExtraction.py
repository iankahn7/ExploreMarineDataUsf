# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 09:05:10 2024
@author: Ian Kahn
This code utilizes datetime_vector_extraction to parse the time vectors out of
t ref times char file.
"""

import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import datetime_vector_extraction as dve

testFlag = True

timeMat = scipy.io.loadmat('tchar.mat')

# Specify the filename of the .mat file
filename = 'tchar.mat'

# Load the time stamps from the file
timeStamps = dve.load_time_stamps(filename)

# Convert datetime objects to vectors
vectors = dve.get_vectors_from_timestamps(timeStamps)

# Define the date range for filtering




# # Define your date range
# start_date = datetime(2000, 1, 1)
# end_date = datetime(2000, 1, 2)


# # Create a mask using a list comprehension
# mask = [(start_date <= ts <= end_date) for ts in timeStamps]

#filter for specific year: 
    
# start_year = 1990
# end_year = 1991


# "***********************************************************"
# mask = [(start_year <= ts[0] <= end_year) for ts in vectors]
# #filter by index 0 which represents year ^
# "***********************************************************"

# # Use np.argwhere to find indices where the condition is True
# indices = np.argwhere(mask).flatten()


# Define your year and month range
target_year = 2000
start_month = 2
end_month = 5

# Filter the vectors by year and month range using mask
mask = [(ts[0] == target_year) and (start_month <= ts[1] <= end_month) for ts in vectors]
filtered_vectors = [vector for vector, include in zip(vectors, mask) if include]

for vector in filtered_vectors:
    print(vector)




# =============================================================================
# # Filter vectors within the specified date range
# filtered_vectors = []
# for vector in vectors:
#     dt = datetime(*vector[:4])  # Convert vector back to datetime object
#     if start_date <= dt <= end_date:
#         filtered_vectors.append(vector)
# 
# =============================================================================



# =============================================================================
# # Display the first 10 vectors within the date range
# numVals = 10
# if testFlag == True:
#     for vector in filtered_vectors[:numVals]:
#         print(vector)
# 
# =============================================================================
