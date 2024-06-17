# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 09:18:29 2024

@author: ikahn
"""

import scipy.io
import matplotlib.pyplot as plt
import numpy as np

# Load the .mat file
mat = scipy.io.loadmat('noaa.mat')
timeMat = scipy.io.loadmat('tchar.mat')

# Access the variables
noaa_raw = mat['noaa_raw']

# Compute the number of data series
#num_series = 5
num_series = noaa_raw.shape[1]
# Initialize correlation matrix
corr_matrix = np.zeros((num_series, num_series))
abs_corrMatrix =  np.zeros((num_series, num_series))
# Compute correlations
for i in range(num_series - 1):
    for j in range(i + 1, num_series):
        # Get data series for i and j
        series_i = noaa_raw[:, i]
        series_j = noaa_raw[:, j]
        
        # Ignore NaN values
        mask = ~np.isnan(series_i) & ~np.isnan(series_j)
        
        if
        series_i = np.nan_to_num(series_i[mask])
        series_j = np.nan_to_num(series_j[mask])
        
        # Compute correlation between data series i and j
        corr_matrix[i, j] = np.corrcoef(series_i, series_j)[0, 1]
        
        #abs value version
        abs_corrMatrix[i,j] = abs(np.corrcoef(series_i, series_j)[0, 1])

# Print the correlation matrix
print("\n Correlation matrix:")
print(corr_matrix)
print("***************************************** /n")
print("\n Absolute Value Correlation matrix:")
print(abs_corrMatrix)



# Plot the correlation matrix
plt.figure()
plt.imshow(corr_matrix, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title('Correlation Matrix of NOAA Raw Data (Ignoring NaNs)')

plt.figure(2)
plt.imshow(abs_corrMatrix, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title('Absolute Value Matrix of NOAA Raw Data (Ignoring NaNs)')


"****************************************************************************"
plt.show()
"****************************************************************************"
