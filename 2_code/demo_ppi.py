import pyart
from matplotlib import pyplot as plt
import numpy as np

filename = '../1_data/KAMX_20140417_1056'
radar = pyart.io.read(filename)

print(radar.fields.keys())

radar = radar.extract_sweeps([0, 1])

#create an instance of the class using our radar
display = pyart.graph.RadarMapDisplay(radar)
#create a Matplotlib figure
f = plt.figure()
#now we are going to do a three panel plot, resolution is a basemap parameter and determines the resolution of
#the coastline.. here we set to intermediate or 'i' ('h' for high 'l' for low)
plt.subplot(1, 3, 1)
display.plot_ppi_map('differential_reflectivity', max_lat = 26.5, min_lat =25.4, min_lon = -81., max_lon = -79.5,
                     vmin = -7, vmax = 7, lat_lines = np.arange(20,28,.2), lon_lines = np.arange(-82, -79, .5),
                     resolution = '110m')
plt.subplot(1, 3, 2)
display.plot_ppi_map('reflectivity', max_lat = 26.5, min_lat =25.4, min_lon = -81., max_lon = -79.5,
                     vmin = -8, vmax = 64, lat_lines = np.arange(20,28,.2), lon_lines = np.arange(-82, -79, .5),
                     resolution = '110m')
"""
plt.subplot(1, 3, 3)
display.plot_ppi_map('velocity', sweep = 1, max_lat = 26.5, min_lat =25.4, min_lon = -81., max_lon = -79.5,
                     vmin = -15, vmax = 15, lat_lines = np.arange(20,28,.2), lon_lines = np.arange(-82, -79, .5),
                     resolution = '110m')
"""
plt.savefig("demo_ppi.png", dpi=200)
