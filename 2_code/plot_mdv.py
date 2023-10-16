#%% Import Module
import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cls
import projection as proj
from pyart.io.mdv_common import MdvFile as read_mdv

#%% Function
def GraphSetUp(field_name:str):
    cb_label    = {
        'DZ':   'Reclectivity (dBZ)',
        'VR':   'Radius Velocity (m/s)',
        'Qr':   'Rain Water Mixing Ratio (g/kg)'
    }
    vrange      = {
        'DZ':   [-1, 66, 1],
        'VR':   [-15, 15, 1],
        'Qr':   [0, 1.5, 0.05]            
    }
    cmap        = {
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
    tick        = {
        'DZ':   np.arange(0, 65+5, 5), 
        'VR':   np.arange(-30, 30+5, 5),
        'Qr':   np.arange(0, 1.5+0.25, 0.25)    
    }
    gs          = {
        'cmap'      : cmap[field_name],
        'vrange'    : vrange[field_name],
        'cb_label'  : cb_label[field_name],
        'tick'      : tick[field_name],
    }
    vmin = gs['vrange'][0]
    vmax = gs['vrange'][1]
    step = gs['vrange'][2]
    gs['levels'] = np.arange(vmin, vmax+step, step)
    gs['norm'] = cls.BoundaryNorm(gs['levels'], ncolors=gs['cmap'].N, clip=True)
    return gs

def PlotRadar(ax, data:tuple, gs:dict):
    import warnings
    warnings.filterwarnings("ignore")
    lon, lat, val = data
    pc = ax.pcolor(lon, lat, val, \
                   cmap=gs['cmap'], norm=gs['norm'], alpha=0.6)
    cb = plt.colorbar(pc, ax=ax, orientation='horizontal', 
                fraction=0.08, pad=0.02, shrink=0.7, aspect=50,
                ticks=gs['tick'])
    cb.ax.tick_params(labelsize=20)
    cb.set_label(label=gs['cb_label'], size=20)

def PlotTW(ax, color:str, linewidth:float):
    from geopandas import read_file as read_shp
    diri = '/mnt/d/TW_GEOG/TW_CITY/COUNTY_MOI_1090820.shp'
    city = read_shp(diri, encoding="utf-8")
    city.boundary.plot(ax=ax, color=color, linewidth=linewidth)
    
def GetFields(MDV):
    fields = {}
    for idx, field_name in enumerate(MDV.fields):
        header = MDV.field_headers[idx]
        nx, ny, nz = (header['nx'], header['ny'], header['nz'])
        dx, dy, dz = (
            header['grid_dx'], header['grid_dy'], header['grid_dz']
        )
        minx, miny, minz = (
            int(header['grid_minx']), 
            int(header['grid_miny']), 
            header['grid_minz']
        )
        x_id, y_id = (
            list(range(minx, minx+nx)),
            list(range(miny, miny+ny))
        )
        x_id_mg, y_id_mg = np.meshgrid(x_id, y_id)
        x, y = (x_id_mg*dx, y_id_mg*dy)
        YLAT, XLON = proj.xy2latlon(header['proj_origin_lat'], \
                                    header['proj_origin_lon'], \
                                    x, y)
        fields[field_name]  = {
            'lat'       : YLAT,
            'lon'       : XLON,
            'lev'       : [h*dz+minz for h in range(nz)],
            'data'      : MDV.read_a_field(idx),
        }
    return fields

def GetRadar(diri:str):
    MDV = read_mdv(diri)
    radar = {}
    radar['clon'] = MDV.radar_info['longitude_deg']
    radar['clat'] = MDV.radar_info['latitude_deg']
    radar['calt'] = MDV.radar_info['altitude_km']
    radar['fields'] = GetFields(MDV)
    return radar

def PlotMDV(info:tuple, items:tuple, save_flag:bool):

    VarName, RadName, Date, Time, HGT, layer= info
    lon, lat, val, clon, clat = items
    data = (lon, lat, val)

    fig, ax = plt.subplots(figsize=(16, 16))
    ax.set_facecolor("#e8edf1")
    dir_gs = {
        'DZ':   GraphSetUp('DZ'),
        'VE':   GraphSetUp('VR'),
        'VR':   GraphSetUp('VR'),
    }
    PlotRadar(ax, data, dir_gs[VarName])

    ##### Plot TW Country Boundary #####
    PlotTW(ax, 'k', 2.)

    ##### Plot radar position #####
    plt.plot(clon, clat, 'ko', markersize=10)

    ##### Title Setting #####
    fig_title = f"{Date} {Time} UTC\n{RadName} / {VarName} / {HGT} km"
    plt.title(fig_title, fontsize=32)

    ##### Domain Setting #####
    lonW, lonE = (120.00, 123.50)
    latS, latN = { 23.00,  26.50}
    plt.xlim(lonW, lonE)
    plt.ylim(latN, latS)
    plt.grid()
    plt.tight_layout()

    ##### Save Fig Setting #####
    if save_flag:
        diro = '../3_result'
        folder = f'{diri[10:-20]}/{Date}/{Time}/{VarName}'
        subprocess.run(['mkdir', '-pv', f'{diro}/{folder}'])
        filename = f'{RadName}_{VarName}_{layer:02}_{Date}T{Time}.png'
        fig_path = f'{diro}/{folder}/{filename}'
        plt.savefig(f"{fig_path}", dpi=200)
        print(f'---> Saved figures as {fig_path}\n')

#%% 
if __name__ == '__main__':

    ##### Input #####
    # diri    = '../1_data/MDV/NU/MDV_test/20211126/050757.mdv'
    # RadName = 'NTU'
    # VarName = 'DZ'
    # layer   = 'all'
    # save_flag = False
    # ------------------------------------------------------------
    diri    = sys.argv[1]
    RadName = sys.argv[2]
    VarName = sys.argv[3]
    layer   = sys.argv[4]
    save_flag = True

    ##### Read MDV #####
    radar = GetRadar(diri)
    Date = diri.split('/')[-2]
    Time = diri.split('/')[-1].split('.')[0]

    lon = radar['fields'][VarName]['lon']
    lat = radar['fields'][VarName]['lat']
    if layer == 'all':
        values = radar['fields'][VarName]['data']
        for L, val in enumerate(values):
            HGT = radar['fields'][VarName]['lev'][L]
            info = (VarName, RadName, Date, Time, HGT, L)
            items = (lon, lat, val, radar['clon'], radar['clat'])
            PlotMDV(info, items, save_flag)
    else:
        HGT = radar['fields'][VarName]['lev'][int(layer)]
        info = (VarName, RadName, Date, Time, HGT, layer)
        val = radar['fields'][VarName]['data'][int(layer)]
        items = (lon, lat, val, radar['clon'], radar['clat'])
        PlotMDV(info, items, save_flag)
    
# %%
