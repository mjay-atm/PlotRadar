#%% Parameter
import numpy as np
earth_radius = 6371000. # meter
deg2rad      = 0.0174532925
rad2deg      = 57.2957795
pi           = 3.14159265359

#%% Function
def xy2latlon(lat0:float, lon0:float, x, y):

    lat0_rad = lat0 * deg2rad
    lon0_rad = lon0 * deg2rad
    x_rad    = np.array([x]) / (earth_radius * 0.001)
    y_rad    = np.array([y]) / (earth_radius * 0.001)

    c = (x_rad**2 + y_rad**2)**(1/2)

    lat = np.ones(x_rad.shape)*np.nan
    lon = np.ones(y_rad.shape)*np.nan

    lat[c != 0.] = np.arcsin(np.cos(c[c != 0.])*np.sin(lat0_rad) + \
              y_rad[c != 0.]*np.sin(c[c != 0.])*np.cos(lat0_rad)/c[c != 0.]) * rad2deg
    lon[c != 0.] = lon0 + np.arctan(x_rad[c != 0.]*np.sin(c[c != 0.])/(c[c != 0.]*np.cos(lat0_rad)*np.cos(c[c != 0.]) - \
                                                                   y_rad[c != 0.]*np.sin(lat0_rad)*np.sin(c[c != 0.]))) * rad2deg

    lat[c == 0.] = lat0
    lon[c == 0.] = lon0

    lat = lat[0]
    lon = lon[0]

    return lat, lon

#%% Test
if __name__ == '__main__':

    lat0 = 23.0
    lon0 = 120.0

    x = [[0, 100], \
         [0, 100]]   # km
    y = [[   0,    0], \
         [-100, -100]]   # km

    lat, lon = xy2latlon(lat0, lon0, x, y)

    print(lat - lat0)
    print(lon - lon0)
# %%
