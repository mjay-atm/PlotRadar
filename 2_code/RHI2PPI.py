#%% Import Modules
import numpy as np
from pyart.io import read_cfradial as read_nc
from pyart.io import write_cfradial as write_nc
from pyart.core.radar import Radar as create_radar

#%% Functions
def CoreRHI2PPI(OLD, nswp, nray):
    NEW = OLD.copy()
    DATA = OLD['data'][:nray].copy()
    NEW['data'] = DATA
    for n in range(0, int(nray/2)):
        N = n//2
        if n % 2:   NEW['data'][n] = OLD['data'][nswp*(2*N+2)-1 ].copy()
        else:       NEW['data'][n] = OLD['data'][nswp*(2*N)     ].copy()
    for n in range(int(nray/2), nray):
        N = (n-int(nray/2))//2
        if n % 2:   NEW['data'][n] = OLD['data'][nswp*(2*N+1)   ].copy()
        else:       NEW['data'][n] = OLD['data'][nswp*(2*N+1)-1 ].copy()
        
    # for n in range(int(nray/4)):
    #     NEW['data'][2*n              ] = OLD['data'][nswp*n+0    ].copy()
    #     NEW['data'][2*n+1            ] = OLD['data'][nswp*(n+2)-1].copy()
    #     NEW['data'][2*n+int(nray/2)  ] = OLD['data'][nswp*(n+1)-1].copy()
    #     NEW['data'][2*n+int(nray/2)+1] = OLD['data'][nswp*(n+1)  ].copy()
    return NEW
#%% Main Script

##### Input #####
diri = '../1_data/NetCDF/cfrad.20211126_045609.000_to_20211126_045609.000_Furuno_W_RHI.nc'
VarName = 'DZ'

##### read_uf #####
NC_OLD = read_nc(diri)

#%% convert rhi to ppi
nswp = int(NC_OLD.nrays/NC_OLD.nsweeps)
nray = NC_OLD.nsweeps*2
time = NC_OLD.time.copy()
time['data'] = NC_OLD.time['data'][:nray].copy() # swp -> ray

#%%
fields = {}
for field_name in NC_OLD.fields:
    # field = NC_OLD.fields[field_name].copy()
    fields[field_name] = CoreRHI2PPI(NC_OLD.fields[field_name], nswp, nray)
    # data = NC_OLD.fields[field_name]['data'][:nray].copy()
    # field['data'] = data
    # for n in range(int(nray/4)):
    #     data[2*n   ] = NC_OLD.fields[field_name]['data'][4*n+1].copy()
    #     data[2*n+60] = NC_OLD.fields[field_name]['data'][4*n+2].copy()
    #     data[2*n+1 ] = NC_OLD.fields[field_name]['data'][4*n+3].copy()
    #     data[2*n+61] = NC_OLD.fields[field_name]['data'][4*n+4].copy()

#%%
swp_numb = NC_OLD.sweep_number.copy()
swp_numb['data'] = NC_OLD.sweep_number['data'][:1].copy()

swp_mode = NC_OLD.sweep_mode.copy()
swp_mode['data'] = NC_OLD.sweep_mode['data'][:1].copy()
string = 'manual_ppi                      ' # must be 32 chars
swp_mode['data'].data[0] = [s.encode('ascii') for s in string]
mask = list(map(str.isspace, string))
swp_mode['data'].mask[0] = mask

#%%
fixed_angle = NC_OLD.fixed_angle.copy()
fixed_angle['data'] = NC_OLD.fixed_angle['data'][:1].copy()
fixed_angle['data'].data[0] = 1.5

#%%
swp_1st_ray_idx = NC_OLD.sweep_start_ray_index.copy()
swp_1st_ray_idx['data'] = NC_OLD.sweep_start_ray_index['data'][:1].copy()

swp_end_ray_idx = NC_OLD.sweep_end_ray_index.copy()
swp_end_ray_idx['data'] = NC_OLD.sweep_end_ray_index['data'][:1].copy()
swp_end_ray_idx['data'].data[0] = nray-1

#%%
# ele = NC_OLD.elevation.copy()
ele = CoreRHI2PPI(NC_OLD.elevation, nswp, nray)
ele['data'][int(nray/2):] = 180 - ele['data'][int(nray/2):]
# for n in range(int(nray/4)):
#     ele['data'][2*n   ] = NC_OLD.elevation['data'][4*n+1].copy()
#     ele['data'][2*n+60] = NC_OLD.elevation['data'][4*n+2].copy()
#     ele['data'][2*n+1 ] = NC_OLD.elevation['data'][4*n+3].copy()
#     ele['data'][2*n+61] = NC_OLD.elevation['data'][4*n+4].copy()

# azi = NC_OLD.azimuth.copy()
azi = CoreRHI2PPI(NC_OLD.azimuth, nswp, nray)
azi['data'][int(nray/2):] = azi['data'][int(nray/2):] + 180
azi['data'][azi['data'] > 360] = azi['data'][azi['data'] > 360] - 360
# for n in range(int(nray/4)):
#     azi['data'][2*n   ] = NC_OLD.azimuth['data'][4*n+1].copy()
#     azi['data'][2*n+60] = NC_OLD.azimuth['data'][4*n+2].copy()
#     azi['data'][2*n+1 ] = NC_OLD.azimuth['data'][4*n+3].copy()
#     azi['data'][2*n+61] = NC_OLD.azimuth['data'][4*n+4].copy()

#%%
instr_paras = NC_OLD.instrument_parameters.copy()
for var in instr_paras:
    if var == 'follow_mode':
        instr_paras[var]['data'] = NC_OLD.instrument_parameters[var]['data'][:1].copy()
    if var == 'pulse_width':
        # instr_paras[var]['data'] = NC_OLD.instrument_parameters[var]['data'][:nray].copy()
        instr_paras[var] = CoreRHI2PPI(NC_OLD.instrument_parameters[var], nswp, nray)
    if var == 'prt_mode':
        instr_paras[var]['data'] = NC_OLD.instrument_parameters[var]['data'][:1].copy()
    if var == 'prt':
        # instr_paras[var]['data'] = NC_OLD.instrument_parameters[var]['data'][:nray].copy()
        instr_paras[var] = CoreRHI2PPI(NC_OLD.instrument_parameters[var], nswp, nray)
    if var == 'prt_ratio':
        # instr_paras[var]['data'] = NC_OLD.instrument_parameters[var]['data'][:nray].copy()
        instr_paras[var] = CoreRHI2PPI(NC_OLD.instrument_parameters[var], nswp, nray)
    if var == 'polarization_mode':
        instr_paras[var]['data'] = NC_OLD.instrument_parameters[var]['data'][:1].copy()
    if var == 'nyquist_velocity':
        # instr_paras[var]['data'] = NC_OLD.instrument_parameters[var]['data'][:nray].copy()
        instr_paras[var] = CoreRHI2PPI(NC_OLD.instrument_parameters[var], nswp, nray)
    if var == 'unambiguous_range':
        # instr_paras[var]['data'] = NC_OLD.instrument_parameters[var]['data'][:nray].copy()
        instr_paras[var] = CoreRHI2PPI(NC_OLD.instrument_parameters[var], nswp, nray)
    if var == 'n_samples':
        # instr_paras[var]['data'] = NC_OLD.instrument_parameters[var]['data'][:nray].copy()
        instr_paras[var] = CoreRHI2PPI(NC_OLD.instrument_parameters[var], nswp, nray)
    if var == 'measured_transmit_power_v':
        # instr_paras[var]['data'] = NC_OLD.instrument_parameters[var]['data'][:nray].copy()
        instr_paras[var] = CoreRHI2PPI(NC_OLD.instrument_parameters[var], nswp, nray)
    if var == 'measured_transmit_power_h':
        # instr_paras[var]['data'] = NC_OLD.instrument_parameters[var]['data'][:nray].copy()
        instr_paras[var] = CoreRHI2PPI(NC_OLD.instrument_parameters[var], nswp, nray)
#%%
rad_calibrate = NC_OLD.radar_calibration.copy()
rad_calibrate['r_calib_index'] = CoreRHI2PPI(NC_OLD.radar_calibration['r_calib_index'], nswp, nray)
# rad_calibrate['r_calib_index']['data'] = NC_OLD.radar_calibration['r_calib_index']['data'][:nray].copy()

#%% 
# scan_rate = NC_OLD.scan_rate.copy()
scan_rate = CoreRHI2PPI(NC_OLD.scan_rate, nswp, nray)
# scan_rate['data'] = NC_OLD.scan_rate['data'][:nray].copy()

#%%
target_scan_rate = NC_OLD.target_scan_rate.copy()
target_scan_rate['data'] = NC_OLD.target_scan_rate['data'][:1].copy()

#%%
# antenna_transition = NC_OLD.antenna_transition.copy()
# antenna_transition['data'] = NC_OLD.antenna_transition['data'][:nray].copy()
antenna_transition = CoreRHI2PPI(NC_OLD.antenna_transition, nswp, nray)
#%%
UF_NEW = create_radar(
    time=time,
    _range                  =   NC_OLD.range.copy(),
    fields                  =   fields,
    metadata                =   NC_OLD.metadata.copy(),
    scan_type               =   'ppi',
    latitude                =   NC_OLD.latitude.copy(),
    longitude               =   NC_OLD.longitude.copy(),
    altitude                =   NC_OLD.altitude.copy(),
    sweep_number            =   swp_numb,
    sweep_mode              =   swp_mode,
    fixed_angle             =   fixed_angle,
    sweep_start_ray_index   =   swp_1st_ray_idx,
    sweep_end_ray_index     =   swp_end_ray_idx,
    azimuth                 =   azi,
    elevation               =   ele,
    scan_rate               =   scan_rate,
    instrument_parameters   =   instr_paras,
    radar_calibration       =   rad_calibrate,
    target_scan_rate        =   target_scan_rate,
    antenna_transition      =   antenna_transition
)

#%%
# print(UF_NEW.info())
print(UF_NEW.info())
# %% Write New UF file
f = write_nc('../1_data/NetCDF/cfrad.20211126_045609.000_to_20211126_045609.000_Furuno_W_PPI.nc', radar=UF_NEW)

#%% Read New UF file
diri = '../1_data/NetCDF/cfrad.20211126_045609.000_to_20211126_045609.000_Furuno_W_PPI.nc'
UF = read_nc(diri)
print(UF.info())
