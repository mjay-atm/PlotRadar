import pyart
import matplotlib.pyplot as plt
def PlotRHI(radar, fig_title:str):

    display = pyart.graph.RadarMapDisplay(radar)

    f = plt.figure(figsize = [12, 9])

    plt.suptitle(fig_title)

    plt.subplot(4, 2, 1)
    display.plot_rhi('total_power',title='Total Reflectivity',
            colorbar_label='dBZ', axislabels=('','Height (km)'))
    plt.ylim([0, 20])

    plt.subplot(4, 2, 2)
    display.plot_rhi('reflectivity', vmin=-5, vmax=75, title='Reflectivity',
            colorbar_label='dBZ', axislabels_flag=False)
    plt.ylim([0, 20])

    plt.subplot(4, 2, 3)
    display.plot_rhi('spectrum_width', vmin=0, vmax=4, title='Doppler Specturm Width',
            colorbar_label='m/s', axislabels=('','Height (km)'))
    plt.ylim([0, 20])

    plt.subplot(4, 2, 4)
    #Nyq_V = radar.instrument_parameters['nyquist_velocity']['data'][0]
    Nyq_V = -99.99
    display.plot_rhi('velocity', vmin=-Nyq_V, vmax=Nyq_V, title=f'Radial Velocity (Nyq.V = {Nyq_V:.2f} m/s)',
            colorbar_label='m/s', axislabels_flag=False)
    plt.ylim([0, 20])

    plt.subplot(4, 2, 5)
    display.plot_rhi('differential_phase', vmin=60, vmax=120, title='Differential Phase ',
            colorbar_label='degree', axislabels=('','Height (km)'))
    plt.ylim([0, 20])

    plt.subplot(4, 2, 6)
    display.plot_rhi('specific_differential_phase', vmin=-2, vmax=2, title='Specific Differential Phase',
            colorbar_label='degrees/km', axislabels_flag=False)
    plt.ylim([0, 20])

    plt.subplot(4, 2, 7)
    display.plot_rhi('cross_correlation_ratio', vmin=0.9, vmax=1.0, title='Cross Correlation Ratio',
            colorbar_label='ratio', axislabels=('Distance (km)', 'Height (km)'))
    plt.ylim([0, 20])

    ##### This block is for UF #####
    plt.subplot(4, 2, 8)
    display.plot_rhi('corrected_differential_reflectivity', vmin=-3, vmax=5, title='Differential Reflectivity',
            colorbar_label='dB', axislabels=('Distance (km)',''))
    plt.ylim([0, 20])

    ##### This block is for RAW #####
    #plt.subplot(4, 2, 8)
    #display.plot_rhi('differential_reflectivity', vmin=-3, vmax=5, title='Differential Reflectivity',
    #        colorbar_label='dB', axislabels=('Distance (km)',''))
    #plt.ylim([0, 20])

    plt.tight_layout()

