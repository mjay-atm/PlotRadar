#%%
import sys
import warnings
import pyart
import cartopy.crs as ccrs
from matplotlib import pyplot as plt

warnings.filterwarnings('ignore')
#%%
# diri = sys.argv[1]
# diri = "../1_data/X-Rock211126050159.RAW0363"
# diri = "../1_data/TEAM-R_211126050159.uf"
# diri = "../1_data/VRQC_TEAM-R_20211126050210_vfbgm.uf"
diri = "../1_data/UF_PNN_TR/uf_PNN_TEAM-R_20211126045526.uf"
print(diri)
radar = pyart.io.read(diri)

print(list(radar.fields.keys()))

#%%
degree_sign = u"\N{DEGREE SIGN}"
for idx, mode in enumerate(radar.sweep_mode['data']):
    print(f'{idx:02} -> {mode.decode("ascii").upper()} {radar.fixed_angle["data"][idx]:.1f}{degree_sign}')
sweep_id_start = int(input("Please input the sweep ID from: "))
sweep_id_end   = int(input("Please input the sweep ID to  : "))

nsweep = sweep_id_end - sweep_id_start + 1
sweep_id = [sweep_id_start + n for n in range(nsweep)]

fields_name = list(radar.fields.keys())
for idy, key in enumerate(fields_name):
    print(f'    {idy} -> {key}')
field_id_start = int(input("    Please input the field ID from: "))
field_id_end   = int(input("    Please input the field ID to  : "))
nfield = field_id_end - field_id_start + 1
field_id = [field_id_start + n for n in range(nfield)]

#%%
for idx in sweep_id:
    sweep = radar.extract_sweeps([idx])

    if sweep.scan_type.upper() == 'PPI':

        scan_start_time = radar.time["units"].split()[-1]
        scan_elevation = sweep.fixed_angle['data'][0]
        print(f'\nPPI at {scan_elevation:.1f}{degree_sign} since {scan_start_time}')

        ##### PLOT FIG #####

        for idy in field_id:

            print("    "+fields_name[idy]+" is plotting...")
            data = sweep.fields[fields_name[idy]]['data'] 
            display = pyart.graph.RadarMapDisplay(sweep)
            
            # Setting projection & ploting the 2nd tilt
            projection = ccrs.LambertConformal(central_latitude=sweep.latitude['data'][0], 
                                               central_longitude=sweep.longitude['data'][0])
            
            fig = plt.figure()
            display.plot_ppi_map(fields_name[idy], resolution = '10m', projection=projection, fig=fig)

            diro = '../3_result/'
            filename = diri.split('/')[-1]
            fig_name = f'{filename.split(".")[0]}_{sweep.scan_type.upper()}_{scan_elevation:.1f}_{fields_name[idy]}.png'
            # plt.savefig(diro+fig_name, dpi=200)
            print('    ===> Saved figure at '+diro+fig_name)

print('\nThis program has ended!!!')

"""
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

plt.subplot(1, 3, 3)
display.plot_ppi_map('velocity', sweep = 1, max_lat = 26.5, min_lat =25.4, min_lon = -81., max_lon = -79.5,
                     vmin = -15, vmax = 15, lat_lines = np.arange(20,28,.2), lon_lines = np.arange(-82, -79, .5),
                     resolution = '110m')

plt.savefig("demo_ppi.png", dpi=200)
"""
