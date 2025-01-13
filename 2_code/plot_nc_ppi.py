#%%
import matplotlib.pyplot as plt
import numpy as np

import pyart
from pyart.testing import get_test_data

# Locate the test data and read in using main read method
# filename = get_test_data("swx_20120520_0641.nc")
filename = '../1_data/NetCDF/cfrad.20211126_045609.000_to_20211126_045609.000_Furuno_W_PPI.nc'
radar = pyart.io.read(filename)
radar.scan_type = 'ppi'
x, y, z = radar.get_gate_x_y_z(0)
x, y, z = (x/1000, y/1000, z/1000)
data = radar.fields['DZ']['data'][:]
#%%

# Setup the display, which automatically detects this is a ppi scan
display = pyart.graph.RadarMapDisplay(radar)
fig, ax = plt.subplots(figsize=(8,7))
# for i in range(30):
#     ax.plot(   x[2*i][::50],    y[2*i][::50], 'k-')
#     ax.plot(   x[4*i][::50],    y[4*i][::50], 'gx')
#     # ax.plot(  -x[2*i][::50],   -y[2*i][::50], 'r--')
#     ax.plot( x[2*i+1][::50],  y[2*i+1][::50], 'r-')
#     ax.plot( x[4*i+1][::50],  y[4*i+1][::50], 'bx')
#     # ax.plot(-x[2*i+1][::50], -y[2*i+1][::50], 'r--')
# ax.plot(   x[60][::50],    y[60][::50], 'mo')
# ax.plot(   x[61][::50],    y[61][::50], 'ro')
# ax.plot(   x[62][::50],    y[62][::50], 'go')
# ax.plot(   x[63][::50],    y[63][::50], 'bo')
# for i in range(0, 30):
#     ax.plot(   x[i][::50],    y[i][::50], 'k-')
# for i in range(30, 60):
#     ax.plot(   x[i][::50],    y[i][::50], 'r-')
# for i in range(60, 90):
#     ax.plot(   x[i][::50],    y[i][::50], 'g-')
# for i in range(90, 120):
#     ax.plot(   x[i][::50],    y[i][::50], 'b-')

ax.set_facecolor('#e8edf1')
# ax.pcolormesh(x[0::2], y[0::2], data[0::2])
# ax.pcolormesh(x[1::2], y[1::2], data[1::2])
ax.pcolormesh(x, y, data)
# display.plot("DZ", 0, vmin=-5, vmax=65.0)
# display.plot_ray("DZ", 10, format_str='k.', ray_min=-5, ray_max=65.0)
# display.plot_range_rings([10, 20, 30, 40])
# display.plot_cross_hair(5.0)
# ax.grid()
# plt.xlim([-10, 10])
# plt.ylim([-10, 10])
plt.show()