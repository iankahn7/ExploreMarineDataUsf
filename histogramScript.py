import scipy.io
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interactive, IntSlider, Layout

# Load the .mat file
mat = scipy.io.loadmat('noaa.mat')

# Access the variables
lat = mat['lat']
lon = mat['lon']
name = mat['name']
noaa_raw = mat['noaa_raw']

# Define a plotting function for the PDF with adaptive binning
def plot_pdf(grabIndex):
    # Extract the site name based on the grabIndex
    site_name = name[grabIndex][0][0]

    # Extract the data for the selected site
    data = noaa_raw[:, grabIndex]

    # Remove NaN values from the data
    data = data[~np.isnan(data)]

    # Calculate the number of bins for bin width of 3
    data_range = np.ptp(data)  # peak-to-peak range
    bins = int(data_range / 3)

    # Create a probability density function (PDF)
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=bins, edgecolor='black', density=True)  # density=True for PDF
    plt.title(f'Probability Density Function (PDF) of Data at {site_name}')
    plt.xlabel('Value')
    plt.ylabel('Probability Density')
    plt.grid(True)
    plt.show()

# Create an interactive plot using ipywidgets
interactive_plot = interactive(plot_pdf,
                               grabIndex=IntSlider(min=0, max=len(name)-1, step=1, value=8, description='Site Index'),
                               layout=Layout(width='100%'))

# Display the interactive plot
interactive_plot
