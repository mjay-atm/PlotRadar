#%% Import Modules
import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cls
from projection import xy2latlon as proj
from pyart.io import read_cfradial as read_uf
from plot_mdv import GraphSetUp

#%% Functions
def PlotTW(ax, color:str, linewidth:float):
    from geopandas import read_file as read_shp
    diri = '/mnt/d/TW_GEOG/TW_CITY/COUNTY_MOI_1090820.shp'
    city = read_shp(diri, encoding="utf-8")
    city.boundary.plot(ax=ax, color=color, linewidth=linewidth)

def PlotTerrain(diri:str, ax):
    from readnc import readnc
    ds, _ = readnc(diri, False)
    HGT = np.array(ds.variables['HGT'][0])
    XLON = np.array(ds.variables['XLONG'][0])
    YLAT = np.array(ds.variables['XLAT'][0])
    tr = ax.contour(XLON, YLAT, HGT, [L*500+250 for L in [0, 2, 4, 6]], colors='k', linestyles='dashed')
    tr = ax.contour(XLON, YLAT, HGT, [L*500+250 for L in [1, 3, 5, 7]], colors='k')
    tr = ax.contourf(XLON, YLAT, HGT, [L*500+250 for L in range(10)], cmap='gray_r')
    return tr

def GetFields(UF):
    fields = {}
    for idx, field_name in enumerate(UF.fields):
        data = UF.fields[field_name]['data'].data.copy()
        mask = UF.fields[field_name]['data'].mask.copy()
        data[mask] = np.nan
        fields[field_name] = {
            'lat':  UF.gate_latitude['data'],
            'lon':  UF.gate_longitude['data'],
            'alt':  UF.gate_altitude['data'],
            'data': data   
        }
    return fields

def GetRadar(diri:str):
    UF = read_uf(diri)
    radar = {
        'clon': UF.longitude['data'][0],
        'clat': UF.latitude['data'][0],
        'calt': UF.altitude['data'][0],
        'fields':   GetFields(UF)
    }
    return radar
#%%
# if __name__ == '__main__':

##### Input #####
# diri = '../1_data/UF/NTU/20211126_045609_Furuno_W_v691217769_RHI.uf'
diri = '../1_data/NetCDF/cfrad.20211126_045609.000_to_20211126_045609.000_Furuno_W_PPI.nc'
# diri = '../1_data/NetCDF/cfrad.20211126_045609.000_to_20211126_045609.000_Furuno_W_RHI.nc'
# diri = '../1_data/NetCDF/20211126_045609_Furuno_W_v9577_SUR.uf'
VarName = 'DZ'

##### Read UF #####
# UF = read_uf(diri)
radar = GetRadar(diri)

#%%
clon = radar['clon']
clat = radar['clat']
lon = radar['fields'][VarName]['lon' ]
lat = radar['fields'][VarName]['lat' ]
val = radar['fields'][VarName]['data']

# LON, LAT = np.meshgrid(lon, lat)

#%%
fig, ax = plt.subplots(figsize=(16,16))
ax.set_facecolor('#e8edf1')
dir_gs = {
    'DZ':   GraphSetUp('DZ'),
    'VE':   GraphSetUp('VR'),
    'VR':   GraphSetUp('VR'),
}
tr = PlotTerrain("../1_data/wrfinput_d03", ax)
gs = GraphSetUp(VarName)
pc = ax.pcolormesh(lon[0::2], lat[0::2], val[0::2], \
               cmap=gs['cmap'], norm=gs['norm'])
# pc = ax.pcolormesh(lon[1::2], lat[1::2], val[1::2], \
#                cmap=gs['cmap'], norm=gs['norm'])
# pc = ax.pcolor(lon, lat, val, \
#                cmap=gs['cmap'], norm=gs['norm'], alpha=0.6)
# st = ax.scatter(lon, lat, c=val, cmap=gs['cmap'], norm=gs['norm'], s=5)
cb = plt.colorbar(pc, ax=ax, orientation='horizontal', 
            fraction=0.08, pad=0.02, shrink=0.7, aspect=50,
            ticks=gs['tick'])
cb.ax.tick_params(labelsize=20)
cb.set_label(label=gs['cb_label'], size=20)

##### Plot TW Country Boundary #####
PlotTW(ax, 'k', 2.)

##### Plot radar position #####
plt.plot(clon, clat, 'k*', markersize=30)

##### Domain Setting #####
lonW, lonE = (121.20, 122.30)
latS, latN = ( 24.20,  25.30)
plt.xlim(lonW, lonE)
plt.ylim(latS, latN)

plt.grid()
plt.tight_layout()
# %%
