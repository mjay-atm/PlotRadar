#%% Library
import numpy as np
import geopandas as gpd
import projection as proj
from matplotlib import pyplot as plt
import matplotlib.colors as cls

#%% Function
def single_max_combine(diri:list, DIM:tuple, missing_flag:bool):
    DATA = []
    ny, nx = DIM
    for fname in diri:
        with open(fname, 'rb') as f:
            array = np.fromfile(f, dtype=np.float32).reshape(ny, nx)
        DATA.append(array.T)
    DATA = np.array(DATA)
    DATA = np.nanmax(DATA, 0)
    if missing_flag: DATA[DATA < -99] = np.nan
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

#%% READ TW_GEOG
# diri = "/mnt/d/TW_GEOG/TW_TOWN/TOWN_MOI_1120317.shp"
# town = gpd.read_file(diri, encoding="utf-8")
# ytwn = town[town['COUNTYNAME'].isin(["宜蘭縣"])]
diri = "/mnt/d/TW_GEOG/TW_CITY/COUNTY_MOI_1090820.shp"
city = gpd.read_file(diri, encoding="utf-8")
# yiln = city[city['COUNTYNAME'].isin(["宜蘭縣"])]

#%% Read Radar Data
diri = "../1_data/CAPPI_TEMR/DZ/cappi_list.txt"
with open(diri, 'r') as f:
    LIST = f.read().splitlines()

DATA = single_max_combine(LIST, (301, 301), False)

radar_name_list = {
    'RCWF': 'RCWF',
    'RCHL': 'RCHL',
    'TEMR': 'TEAM-R'
}
radar_name = radar_name_list[diri.split('/')[-3].split('_')[-1]]
# print(radar_name)

radar_position = {
    'RCWF': (25.07306, 121.77306),
    'RCHL': (23.99000, 121.62000),
    'TEMR': (24.82083, 121.72861)
}
lat0, lon0 = radar_position[diri.split('/')[-3].split('_')[-1]]

dy, dx = (1., 1.) # km
ny, nx = DATA.shape
x_id = list(range(-(nx//2), nx//2+1))
y_id = list(range(-(ny//2), ny//2+1))
x_id_mg, y_id_mg = np.meshgrid(x_id, y_id)
x, y = (x_id_mg*dx, y_id_mg*dy)
YLAT, XLON = proj.xy2latlon(lat0, lon0, x, y)

#%% PLOT
##### Domain Setting #####
# lonE = 123.50
# lonW = 118.50
# latS = 21.50
# latN = 26.50
lonE = 123.50
lonW = 120.00
latS = 23.00
latN = 26.50

##### PLOT SETTING #####
cb_label = {
    'DZ':   'Reclectivity (dBZ)',
    'VR':   'Radius Velocity (m/s)',
    'Qr':   'Rain Water Mixing Ratio (g/kg)'
}

vrange = {
    'DZ':   [-1, 66, 1],
    'VR':   [-15, 15, 1],
    'Qr':   [0, 1.5, 0.05]
}

cmap = {
    'DZ':   cls.ListedColormap(colors = ['#FFFFFF', \
                                        '#00FFFF', '#00ECFF', '#00DAFF', '#00C8FF', '#00B6FF', \
                                        '#00A3FF', '#0091FF', '#007FFF', '#006DFF', '#005BFF', \
                                        '#0048FF', '#0036FF', '#0024FF', '#0012FF', '#0000FF', \
                                        '#00FF00', '#00F400', '#00E900', '#00DE00', '#00D300', \
                                        '#00C800', '#00BE00', '#00B400', '#00AA00', '#00A000', \
                                        '#009600', '#33AB00', '#66C000', '#99D500', '#CCEA00', \
                                        '#FFFF00', '#FFF400', '#FFE900', '#FFDE00', '#FFD300', \
                                        '#FFC800', '#FFB800', '#FFA800', '#FF9800', '#FF8800', \
                                        '#FF7800', '#FF6000', '#FF4800', '#FF3000', '#FF1800', \
                                        '#FF0000', '#F40000', '#E90000', '#DE0000', '#D30000', \
                                        '#C80000', '#BE0000', '#B40000', '#AA0000', '#A00000', \
                                        '#960000', '#AB0033', '#C00066', '#D50099', '#EA00CC', \
                                        '#FF00FF', '#EA00FF', '#D500FF', '#C000FF', '#AB00FF', \
                                        '#FFC8FF']),
    'VR':   plt.colormaps['bwr'],
    'Qr':   plt.colormaps['terrain_r']
}

tick = {
    'DZ':   np.arange(0, 65+5, 5), 
    'VR':   np.arange(-30, 30+5, 5),
    'Qr':   np.arange(0, 1.5+0.25, 0.25)
}

var_name = diri.split('/')[-2]
vmin = vrange[var_name][0]
vmax = vrange[var_name][1]
step = vrange[var_name][2]
levels = np.arange(vmin, vmax+step, step)
cmap = cmap[var_name]
norm = cls.BoundaryNorm(levels, ncolors=cmap.N, clip=True)

degree_sign = u"\N{DEGREE SIGN}"

##### PLOTTING #####
fig, ax = plt.subplots(figsize=(16, 16))

city.boundary.plot(ax=ax, color='k', linewidth=2.)
# yiln.boundary.plot(ax=ax, color='r', linewidth=3)

# ax = plot_domain(24.8200, 122.0300, 1., 1., 200, 200, 'g-')     # 200px_482-203_it100
# ax = plot_domain(24.8200, 121.7300, 1., 1., 200, 200, 'r')     # 200px_482-173_it100
# ax = plot_domain(24.8200, 121.7300, 1., 1., 300, 200, 'b')     # 300x200_482-173_it100
# ax = plot_domain(24.3200, 121.7300, 1., 1., 300, 300, 'g')     # 300x300_482-173_it100
# ax = plot_domain(24.9470, 121.77306, 1., 1., 300, 300, 'r')
# ax = plot_domain(24.8470, 121.7730, 1., 1., 200, 200, 'r-')
ax = plot_domain(24.8470, 121.7730, 1., 1., 300, 300, 'r-')     # 300px_484-177_*
# ax = plot_domain(23.5124, 122.2998, 1., 1., 500, 500, 'k')      # Old WRF Background
# ax = plot_domain(24.04555, 121.4224, 1., 1., 500, 500, 'k')     # New WRF Background

Radar = radar_name.upper()
ax.set_facecolor("#e8edf1")
ax.plot(lon0, lat0, "ro", label=Radar, markersize=10)

lon, lat, data = (XLON, YLAT, DATA)
pc = plt.pcolor(lon, lat, data,
            cmap=cmap, norm=norm, alpha=0.6)

cb = plt.colorbar(pc, ax=ax, orientation='horizontal', 
                fraction=0.08, pad=0.02, shrink=0.7, aspect=50,
                ticks=tick[var_name])
cb.ax.tick_params(labelsize=20)
cb.set_label(label=cb_label[var_name], size=20)

##### View Domain Setting #####
fig_title = f"CAPPI MAX COMBINE / {radar_name} / {var_name}"
plt.xlim(lonW, lonE)
plt.ylim(latS, latN)
plt.grid()
plt.title(fig_title, fontsize=32)
plt.tight_layout()
# %%
