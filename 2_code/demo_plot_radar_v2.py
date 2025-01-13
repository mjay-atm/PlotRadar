import sys
import pyart
from matplotlib import pyplot as plt
from PlotRHI import PlotRHI

def PlotPPI(radar, fig_title):

    display = pyart.graph.RadarMapDisplay(radar)
    
    f = plt.figure()
    
  #  plt.suptitle(fig_title)
    
    plt.subplot(2, 4, 1)
    display.plot_ppi_map('total_power',title='Total Reflectivity', 
            colorbar_label='dBZ')
    plt.ylim([0, 20])
    
    plt.subplot(2, 4, 2)
    display.plot_ppi_map('reflectivity', vmin=-5, vmax=75, title='Reflectivity', 
            colorbar_label='dBZ')
    plt.ylim([0, 20])
    
    plt.subplot(2, 4, 3)
    display.plot_ppi_map('spectrum_width', vmin=0, vmax=4, title='Doppler Specturm Width', 
            colorbar_label='m/s')
    plt.ylim([0, 20])
    
    plt.subplot(2, 4, 4)
    Nyq_V = radar.instrument_parameters['nyquist_velocity']['data'][0]
    display.plot_ppi_map('velocity', vmin=-Nyq_V, vmax=Nyq_V, title=f'Radial Velocity (Nyq.V = {Nyq_V:.2f} m/s)', 
            colorbar_label='m/s')
    plt.ylim([0, 20])
    
    plt.subplot(2, 4, 5)
    display.plot_ppi_map('differential_phase', vmin=60, vmax=120, title='Differential Phase ', 
            colorbar_label='degree')
    plt.ylim([0, 20])
    
    plt.subplot(2, 4, 6)
    display.plot_ppi_map('specific_differential_phase', vmin=-2, vmax=2, title='Specific Differential Phase', 
            colorbar_label='degrees/km')
    plt.ylim([0, 20])
    
    plt.subplot(2, 4, 7)
    display.plot_ppi_map('cross_correlation_ratio', vmin=0.9, vmax=1.0, title='Cross Correlation Ratio', 
            colorbar_label='ratio')
    plt.ylim([0, 20])
    
    ##### This block is for UF #####
   # plt.subplot(2, 4, 8)
   # display.plot_ppi_map('corrected_differential_reflectivity', vmin=-3, vmax=5, title='Differential Reflectivity', 
   #         colorbar_label='dB', axislabels=('Distance (km)',''))
   #  plt.ylim([0, 20])
    
    ##### This block is for RAW #####
    plt.subplot(2, 4, 8)
    display.plot_ppi_map('differential_reflectivity', vmin=-3, vmax=5, title='Differential Reflectivity', 
            colorbar_label='dB')
    plt.ylim([0, 20])
    plt.tight_layout()

# diri = '/home/physic2/AS/Radar_Lab/Code_demo/1_data/'
# filename = 'TMR220711225934.RAWSDHM'
# radar = pyart.io.read_uf(diri+filename)

diri = sys.argv[1]
print(diri)
radar = pyart.io.read(diri)
print(radar.info())

degree_sign = u"\N{DEGREE SIGN}"
for idx, mode in enumerate(radar.sweep_mode['data']):
    print(f'{idx} -> {mode.decode("ascii").upper()} {radar.fixed_angle["data"][idx]:02}{degree_sign}')
sweep_id_start = int(input("Please input the sweep ID from: "))
sweep_id_end   = int(input("Please input the sweep ID to  : "))

nsweep = sweep_id_end - sweep_id_start + 1
sweep_id = [sweep_id_start + n for n in range(nsweep)]

for idx in sweep_id:
    sweep = radar.extract_sweeps([idx])
    print(sweep.info())
    # print(sweep.scan_type.upper())
    if sweep.scan_type.upper() == 'RHI':

        scan_start_time = radar.time["units"].split()[-1] #some bugs in this line as the start time of each sweep is diff.
        scan_fixed_angle = sweep.fixed_angle["data"][0]
        fig_title = f'RHI at {scan_fixed_angle:.1f}{degree_sign} since {scan_start_time}'
        
        print(f'\nPlotting {fig_title} ...')
        PlotRHI(sweep, fig_title)
        
        """
        data = sweep.fields['total_power']['data']
        print(data)

        fig = plt.figure()
        plt.contourf(data)
        
        diro = '../3_result/'
        filename = diri.split('/')[-1]
        fig_name = f'{filename.split(".")[0]}_RHI_{scan_fixed_angle:.1f}.png'
        """
        
    elif sweep.scan_type.upper() == 'PPI':

        scan_start_time = radar.time["units"].split()[-1]
        scan_fixed_angle = sweep.fixed_angle['data'][0]
        print(f'\nPPI at {scan_fixed_angle}{degree_sign} since {scan_start_time}')

    diro = '../3_result/'
    filename = diri.split('/')[-1]
    fig_name = f'{filename.split(".")[0]}_{sweep.scan_type.upper()}_{scan_fixed_angle:.1f}_v2.png'
    plt.savefig(diro+fig_name, dpi=200, bbox_inches='tight')
    print('Saved figure at '+diro+fig_name)

print('\nAll done!!!')
