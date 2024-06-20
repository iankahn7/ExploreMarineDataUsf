# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 12:06:41 2024

@author:  Ian Kahn
    
"""
import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
testingFlag = False

"***************************************************************************"
# Load the .mat file containing time references
timeMat = scipy.io.loadmat('tchar.mat')
t_ref_char = timeMat['t_ref_char']

# Convert datetime strings to datetime objects
timeStamps = [datetime.strptime(t, '%m/%d/%Y %H:') for t in t_ref_char]

# Function to convert datetime object to its components
def datetime_to_vector(dt):
    return [dt.year, dt.month, dt.day, dt.hour]

# Apply the function to each datetime object in the timeStamps list
vectors = [datetime_to_vector(dt) for dt in timeStamps]

# Display the vectors
if testingFlag == True:
    for vector in vectors:
        print(vector)