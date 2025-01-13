#%% Import Module
from pyart.io import read as read_rad

#%% Read Radar Data
diri = ''
radar = read_rad(diri)