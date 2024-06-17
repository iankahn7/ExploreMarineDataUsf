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
#num_series = noaa_raw.shape[1]
num_series = 5

# Initialize correlation matrix
corr_matrix = np.zeros((num_series, num_series))

# Compute correlations
i = 0
j = 0
for i in range(num_series - 1):
    j = i + 1
    for j in range(num_series):
        # correlation here , find where there are overlaps 
        #pull out 2 time series for i and j
        
        # corrcoef Return Pearson product-moment correlation coefficients.
        corr_matrix[i, j] = np.corrcoef(noaa_raw[:, i], noaa_raw[:, j])[0, 1]

# Print the correlation matrix
print("\nCorrelation matrix:")
print(corr_matrix)

# Plot the correlation matrix
plt.figure()
plt.imshow(corr_matrix, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title('Correlation Matrix of NOAA Raw Data')
plt.show()
