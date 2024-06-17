# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 09:18:29 2024

@author: ikahn
"""
import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Load the .mat file
mat = scipy.io.loadmat('noaa.mat')
timeMat = scipy.io.loadmat('tchar.mat')

# Access the variables
noaa_raw = mat['noaa_raw']

# Compute the number of data series
#num_series = 5
num_series = noaa_raw.shape[1]



"""
ecorr_matrix = np.zeros((num_series, num_series))
abs_corrMatrix =  np.zeros((num_series, num_series))
"""

"""
 You can initialize the corr_matrix and abs_corrMatrix with NaNs 
 instead of zeros by using np.full to create arrays filled with np.nan
"""
# Initialize correlation matrix
corr_matrix = np.full((num_series, num_series), np.nan)
abs_corrMatrix = np.full((num_series, num_series), np.nan)
numPts = np.full((num_series, num_series), np.nan)
# Compute correlations
minNumPoints = 1000
for i in range(num_series - 1):
    for j in range(i + 1, num_series):
        # Get data series for i and j
        series_i = noaa_raw[:, i]
        series_j = noaa_raw[:, j]
        
        # Ignore NaN values
        mask = ~np.isnan(series_i) & ~np.isnan(series_j)
        
        #if number of values in mask is greater than 1000, then do the below
        
        if np.sum(mask) > minNumPoints:
            series_i = np.nan_to_num(series_i[mask])
            series_j = np.nan_to_num(series_j[mask])
        
            # Compute correlation between data series i and j
            corr_matrix[i, j] = np.corrcoef(series_i, series_j)[0, 1]
            
            #abs value version
            abs_corrMatrix[i,j] = abs(np.corrcoef(series_i, series_j)[0, 1])
            
            numPts[i,j] = np.sum(mask)
            

# Print the correlation matrix
print("\n Correlation matrix:")
print(corr_matrix)
print("***************************************** /n")
print("\n Absolute Value Correlation matrix:")
print(abs_corrMatrix)



# Plot the correlation matrix
plt.figure()
plt.imshow(corr_matrix, cmap='rainbow', interpolation='nearest')
plt.colorbar()
plt.title(f'Correlation NOAA Raw Data (minNumPoints = {minNumPoints})')

plt.figure(2)
plt.imshow(abs_corrMatrix, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title(f'Absolute Value NOAA Raw Data (minNumPoints = {minNumPoints})')

plt.figure(3)
plt.imshow(numPts, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title(f' numpoints (minNumPoints = {minNumPoints})')



# Example usage with the provided matrices and minNumPoints value

"****************************************************************************"
plt.show()
"****************************************************************************"
def plot_corr_insights(corr_matrix, abs_corrMatrix, numPts, minNumPoints, save_dir='.'):
    # Function to plot and provide insights into the correlation matrices
    
    def plot_matrix(matrix, title, cmap='rainbow', log_scale=False, dpi=300):
        plt.figure(figsize=(10, 8))
        if log_scale:
            matrix_log = np.copy(matrix)
            matrix_log[matrix_log <= 0] = 1e-10  # Avoid log of zero or negative values
            plt.imshow(matrix_log, cmap=cmap, interpolation='nearest', norm=mcolors.LogNorm())
        else:
            plt.imshow(matrix, cmap=cmap, interpolation='nearest')
        plt.colorbar()
        plt.title(title)
        
        # Calculate and annotate descriptive statistics
        mean_val = np.nanmean(matrix)
        median_val = np.nanmedian(matrix)
        std_val = np.nanstd(matrix)
        plt.xlabel('Series Index')
        plt.ylabel('Series Index')
        plt.text(0.95, 0.01, f'Mean: {mean_val:.2f}\nMedian: {median_val:.2f}\nStd: {std_val:.2f}',
                 verticalalignment='bottom', horizontalalignment='right',
                 transform=plt.gca().transAxes,
                 color='white', fontsize=12, bbox=dict(facecolor='black', alpha=0.5))
        
        # Save the figure as a JPEG file with the title as filename
        filename = title.replace(' ', '_').replace(':', '').replace('(', '').replace(')', '')
        plt.savefig(os.path.join(save_dir, f"{filename}.jpg"), format='jpeg',dpi = dpi)
        plt.show()
        
        # Plot histogram of values
        plt.figure(figsize=(10, 4))
        plt.hist(matrix[~np.isnan(matrix)].flatten(), bins=50, color='blue', edgecolor='black')
        plt.title(f'Histogram of {title}')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        
        # Save the histogram as a JPEG file with the title as filename
        plt.savefig(os.path.join(save_dir, f"{filename}_hist.jpg"), format='jpeg', dpi = dpi)
        plt.show()
    
    # Plot and analyze the correlation matrix
    plot_matrix(corr_matrix, f'Correlation NOAA Raw Data (minNumPoints = {minNumPoints})', cmap='rainbow', log_scale=True)
    
    # Plot and analyze the absolute value correlation matrix
    plot_matrix(abs_corrMatrix, f'Absolute Value NOAA Raw Data (minNumPoints = {minNumPoints})', cmap='hot', log_scale=False)
    
    # Plot and analyze the number of points matrix
    plot_matrix(numPts, f'Number of Points (minNumPoints = {minNumPoints})', cmap='hot', log_scale=False)

# Example usage with the provided matrices and minNumPoints value

def identify_high_correlation_stations(corr_matrix, threshold=0.8):
    """
    Identify stations with high correlation.
    
    Parameters:
    corr_matrix (numpy.ndarray): Correlation matrix.
    threshold (float): Threshold for identifying high correlation.
    
    Returns:
    list: List of tuples with indices of stations that have high correlation.
    """
    high_corr_stations = []
    num_series = corr_matrix.shape[0]
    
    for i in range(num_series - 1):
        for j in range(i + 1, num_series):
            if np.abs(corr_matrix[i, j]) >= threshold:
                high_corr_stations.append((i+1, j+1))
    
    return high_corr_stations

# Example usage with the provided correlation matrix and threshold
high_corr_stations = identify_high_correlation_stations(abs_corrMatrix, threshold=0.8)
print(f"Stations with high correlation (threshold=0.8): {high_corr_stations}")

save_directory = 'C:\\Users\\ikahn\\Desktop\\unm\\IanKahn_RESUMES\\ocean_sci\\usf_making_waves\\Research\\screenshots' # Specify your directory here
plot_corr_insights(corr_matrix, abs_corrMatrix, numPts, minNumPoints, save_dir=save_directory)
