#%% Import Modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cls
from geopandas import read_file as read_shp
from pyart.io import read as read_rad
#%% Read Geo Data
diri = "/mnt/d/TW_GEOG/TW_CITY/COUNTY_MOI_1090820.shp"
city = read_shp(diri, encoding="utf-8")

#%% Read Radar Data
##### TEAM-R ##### 
# diri = "../1_data/UF_TR/0_ORG/20211126_045537_TEAM-R_v117_SUR.uf"
# diri = "../1_data/UF_TR/1_NNN/uf_NNN_20211126_045537_TEAM-R_v117_SUR.uf"
# diri = "../1_data/UF_TR/2_TNN/uf_TNN_20211126_045537_TEAM-R_v117_SUR.uf"
# diri = "../1_data/UF_TR/3_PNN/uf_PNN_20211126_045537_TEAM-R_v117_SUR.uf"
# diri = "../1_data/UF_TR/4_PSN/uf_PSN_20211126_045537_TEAM-R_v117_SUR.uf"
# diri = "../1_data/UF_TR/5_PSS/uf_PSS_20211126_045537_TEAM-R_v117_SUR.uf"
# diri = "../1_data/VRQC_TEAM-R_20211126045537_test.uf"
# diri = "../1_data/uf_NNN_VRQC_TEAM-R_20211126045537_test.uf"
##### RCWF #####
# diri = "../1_data/UF_WF/0_ORG/20211126_045723_RCWF_v031_SUR.uf"
# diri = "../1_data/UF_WF/1_NNN/uf_NNN_20211126_045723_RCWF_v031_SUR.uf"
# diri = "../1_data/UF_WF/2_TNN/uf_TNN_20211126_045723_RCWF_v031_SUR.uf"
# diri = "../1_data/UF_WF/3_PNN/uf_PNN_20211126_045723_RCWF_v031_SUR.uf"
# diri = "../1_data/UF_WF/4_PSN/uf_PSN_20211126_045723_RCWF_v031_SUR.uf"
diri = "../1_data/UF_WF/5_PSS/uf_PSS_20211126_045723_RCWF_v031_SUR.uf"
# diri = "../1_data/VRQC_TEAM-R_20211126045537_test.uf"
# diri = "../1_data/uf_NNN_VRQC_TEAM-R_20211126045537_test.uf"
radar = read_rad(diri)

#%% Print Info
degree_sign = u"\N{DEGREE SIGN}"
for idx, mode in enumerate(radar.sweep_mode['data']):
    ielev = idx
    modes = mode.decode("ascii").upper()
    angle = radar.fixed_angle["data"][idx]
    print(f'{ielev:02} -> {modes} {angle:4.1f}{degree_sign}')
swp_st = int(input("Please input the sweep ID from: "))
swp_ed = int(input("Please input the sweep ID to  : "))
nswp = swp_ed - swp_st + 1
iswp = [swp_st + n for n in range(nswp)]
print()

var_name = list(radar.fields.keys())
for idy, key in enumerate(var_name):
    print(f'{idy:02} -> {key}')
var_st = int(input("Please input the field ID from: "))
var_ed = int(input("Please input the field ID to  : "))
nvar = var_ed - var_st + 1
ivar = [var_st + n for n in range(nvar)]

#%% Plot
data = radar.get_field(iswp[0], var_name[ivar[0]], True)
lat, lon, alt = radar.get_gate_lat_lon_alt(iswp[0])

##### PLOT SETTING #####
cb_label = {
    'reflectivity':   'Reclectivity (dBZ)',
    'velocity':   'Radius Velocity (m/s)',
    'corrected_velocity':   'Radius Velocity (m/s)',
    'Qr':   'Rain Water Mixing Ratio (g/kg)'
}

vrange = {
    'reflectivity':   [-1, 66, 1],
    'velocity':   [-15, 15, 1],
    'corrected_velocity':   [-31, 31, 1],
    'Qr':   [0, 1.5, 0.05]
}

cmap = {
    'reflectivity':   cls.ListedColormap(colors = ['#FFFFFF', \
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
    'velocity':   plt.colormaps['bwr'],
    'corrected_velocity':   plt.colormaps['bwr'],
    'Qr':   plt.colormaps['terrain_r']
}

tick = {
    'reflectivity':   np.arange(0, 65+5, 5), 
    'velocity':   np.arange(-30, 30+5, 5),
    'corrected_velocity':   np.arange(-30, 30+5, 5),
    'Qr':   np.arange(0, 1.5+0.25, 0.25)
}

var_name = var_name[ivar[0]]
vmin = vrange[var_name][0]
vmax = vrange[var_name][1]
step = vrange[var_name][2]
levels = np.arange(vmin, vmax+step, step)
cmap = cmap[var_name]
norm = cls.BoundaryNorm(levels, ncolors=cmap.N, clip=True)

radar_code = 'TEMR'

radar_position = {
    'RCWF': (25.07306, 121.77306),
    'RCHL': (23.99000, 121.62000),
    'TEMR': (24.82083, 121.72861)
}
lat0, lon0 = radar_position[radar_code]

radar_name_list = {
    'RCWF': 'RCWF',
    'RCHL': 'RCHL',
    'TEMR': 'TEAM-R'
}
radar_name = radar_name_list[radar_code]

lonE = 123.50
lonW = 120.00
latS = 23.00
latN = 26.50

##### PLOTTING #####
fig, ax = plt.subplots(figsize=(16, 16))

city.boundary.plot(ax=ax, color='k', linewidth=2.)

ax.set_facecolor("#e8edf1")
ax.plot(lon0, lat0, "ro", label=radar_name, markersize=10)

pc = plt.pcolor(lon, lat, data,
            cmap=cmap, norm=norm, alpha=0.6)

cb = plt.colorbar(pc, ax=ax, orientation='horizontal', 
                fraction=0.08, pad=0.02, shrink=0.7, aspect=50,
                ticks=tick[var_name])
cb.ax.tick_params(labelsize=20)
cb.set_label(label=cb_label[var_name], size=20)

##### View Domain Setting #####
fig_title = f"PPI 0.5{degree_sign} / {radar_name} / {var_name}"
plt.xlim(lonW, lonE)
plt.ylim(latS, latN)
plt.grid()
plt.title(fig_title, fontsize=32)
plt.tight_layout()
# %%
