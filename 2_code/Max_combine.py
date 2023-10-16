#%% Library
import sys
import numpy as np
import geopandas as gpd
import projection as proj
import matplotlib.colors as cls
from matplotlib import pyplot as plt
from plot_mdv import GraphSetUp
from plot_mdv import PlotTW
#%% Classes
class ReadRakitCAPPI:
    def __init__(self) -> None:
        pass
    def read(self, diri:list, dim:tuple):
        ny, nx = dim
        radar = []
        for fn in diri:
            with open(fn, 'rb') as f:
                array = np.fromfile(f, dtype=np.float32).reshape(ny, nx)
            radar.append(array.T)
        radar = np.array(radar)
        radar[radar < -99] = np.nan
        return radar

class ReadMDV:
    def __init__(self) -> None:
        pass
    def read(self, diri:str):
        from pyart.io.mdv_common import MdvFile as read_mdv
        MDV = read_mdv(diri)
        radar = self._GetFieldValue(MDV)
        return radar
    def _GetFieldValue(self, MDV):
        data = None
        for idx, var in enumerate(MDV.fields):
            if var == 'DZ':
                data = MDV.read_a_field(idx)
        if data is None: raise Exception("Reflectivity cannot found in MDV file")
        return data

#%% Function          
def single_max_combine(diri, filetype:str, **kwargs):
    dir_radar = {
        'Rakit' : "ReadRakitCAPPI().read(diri, kwargs['DIM'])",
        'MDV'   : "ReadMDV().read(diri)"
    }
    radar = eval(dir_radar[filetype])
    DATA = np.nanmax(radar, 0)
    return DATA

def plot_domain(clat, clon, dx, dy, nx, ny, color):
    x_id = list(range(-(nx//2), nx//2+1))
    y_id = list(range(-(ny//2), ny//2+1))
    corner_x_id = np.array([x_id[0], x_id[0], x_id[-1], x_id[-1], x_id[0]]) * dx
    corner_y_id = np.array([y_id[0], y_id[-1],y_id[-1], y_id[0] , y_id[0]]) * dy
    CY, CX = proj.xy2latlon(clat, clon, corner_x_id, corner_y_id)
    ax.plot(CX, CY, f'{color}-', linewidth=4)
    ax.plot(clon, clat, f"{color}+", markersize=20)
    return ax

def RadarInfo(name:str):
    LongNameList = {
        'RCWF': 'RCWF',
        'RCHL': 'RCHL',
        'TEMR': 'TEMR',
        'Furu': 'NTU X-pol'
    }
    Position = {
        'RCWF': (25.07306, 121.77306),
        'RCHL': (23.99000, 121.62000),
        'TEMR': (24.82083, 121.72861),
        'Furu': (24.73250, 121.75472)
    }
    Info = {
        'namelist'  : LongNameList[name],
        'position'  : Position[name]
    }
    return Info

def GetLatLon(DataShape:tuple, resolution:tuple, Center:tuple):
    ny, nx = DataShape
    dy, dx = resolution
    clat, clon  = Center
    x_id = list(range(-(nx//2), nx//2+1))
    y_id = list(range(-(ny//2), ny//2+1))
    x_id_mg, y_id_mg = np.meshgrid(x_id, y_id)
    x, y = (x_id_mg*dx, y_id_mg*dy)
    YLAT, XLON = proj.xy2latlon(clat, clon, x, y)
    return YLAT, XLON


#%% Read Radar Data
diri = "../1_data/MDV/TR/VRQC/1_NNN/20211126/045957.mdv"
DATA = single_max_combine(diri, 'MDV', DIM=None)
RadName = "TEMR"
# ------------------------------------------------------------
# diri = "../1_data/CAPPI_TEMR/DZ/cappi_list.txt"
# with open(diri, 'r') as f:
#     LIST = f.read().splitlines()
# DATA = single_max_combine(LIST, 'Rakit', DIM=(301, 301))
# RadName = 'Furu'
# ------------------------------------------------------------
# diri = sys.argv[1]
# RadName = sys.argv[2]
# FileType = sys.argv[3]
# DIM = sys.argv[4]

#%% PLOT
RI = RadarInfo(RadName)
radar_name = RI['namelist']
lat0, lon0 = RI['position']
YLAT, XLON = GetLatLon(DATA.shape, (1., 1.), (lat0, lon0))
Radar = radar_name.upper()
VarName = 'DZ'
fig_title = f"CAPPI MAX COMBINE / {radar_name} / {VarName}"

##### Domain Setting #####
lonE, lonW, latS, latN = (123.5, 120.0, 23.0, 26.5)

##### PLOTTING #####
gs = GraphSetUp(VarName)
fig, ax = plt.subplots(figsize=(16, 16))
ax.set_facecolor("#e8edf1")

##### Plot TW Country Boundary #####
PlotTW(ax, 'k', 2.)

##### Plot Simulation Domain #####
ax = plot_domain(24.8470, 121.7730, 1., 1., 300, 300, 'r-')     # 300px_484-177_*

##### Plot Radar Location #####
ax.plot(lon0, lat0, "ko", label=Radar, markersize=10)

##### Plot Radar Data #####
lon, lat, data = (XLON, YLAT, DATA)
pc = plt.pcolor(lon, lat, data,
            cmap=gs['cmap'], norm=gs['norm'], alpha=0.6)
cb = plt.colorbar(pc, ax=ax, orientation='horizontal', 
                fraction=0.08, pad=0.02, shrink=0.7, aspect=50,
                ticks=gs['tick'])
cb.ax.tick_params(labelsize=20)
cb.set_label(label=gs['cb_label'], size=20)

##### View Domain Setting #####
plt.xlim(lonW, lonE)
plt.ylim(latS, latN)
plt.grid()
plt.title(fig_title, fontsize=32)
plt.tight_layout()
# %%
