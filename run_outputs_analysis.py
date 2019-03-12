import yaml
import xray
from matplotlib import pyplot as plt
from plot_results import *
from output_analysis import *

if __name__ == "__main__":
    # array_to_process = [
    #     'results/netcdf_files/ww3_hycom.2015.nc',
    #     # 'results/netcdf_files/ww3_hycom.2015.nc',
    #     # 'results/netcdf_files/ww3_hycom.2016.nc',
    #     'results/netcdf_files/ww3_mercator.2014.nc',
    #     # 'results/netcdf_files/ww3_mercator.2015.nc',
    #     # 'results/netcdf_files/ww3_mercator.2016.nc',
    #     'results/netcdf_files/ww3_globcurtot.2014.nc',
    #     # 'results/netcdf_files/ww3_globcurtot.2015.nc',
    #     # 'results/netcdf_files/ww3_globcurtot.2016.nc'
    # ]
    
    # ww3_cur_path = 'results/netcdf_files/ww3_nocur.2015.nc'
    # ww3_cur = xray.open_dataset('results/netcdf_files/ww3_hycom.2014_ef.nc')
    # ww3_cur = xray.open_dataset('results/netcdf_files/ww3_mercator.2014.nc')
    
    # ww3_no_cur_path = 'results/netcdf_files/ww3_nocur.2014.nc'
    # ww3_no_cur = xray.open_dataset('results/netcdf_files/ww3_nocur.2014_ef.nc')
    
    # pnboia_path = 'http://goosbrasil.org:8080/pnboia/Bcabo_frio2.nc'
    # pnboia_path = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Bsantos2.nc') # 2017
    # pnboia_path = 'http://goosbrasil.org:8080/pnboia/Bsantos.nc' # 2014-11-15 - 2017-04-06
    # pnboia_path = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Bguanabara2.nc') # 2017
    # pnboia_path = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Bguanabara.nc')
    # pnboia_path = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Bsanta_catarina2.nc') # 2017
    # 'http://goosbrasil.org:8080/pnboia/Bsanta_catarina.nc'
    # pnboia_path = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Brio_grande2.nc') # 2017
    pnboia_path = 'http://goosbrasil.org:8080/pnboia/Brio_grande.nc'
    
    # hycom_path, mercator_path, globcurtot_path = array_to_process
    
    hycom_path = 'results/netcdf_files/ww3_hycom.2016.nc'
    ww3_cur_path = 'results/netcdf_files/ww3_nocur.2016.nc'
    
    ana = OutputAnalysis(hycom_path, ww3_cur_path, pnboia_path)
    # import pdb; pdb.set_trace()
    ana.check_vel_pnboia(-46.3, -27)
    
    # import pdb; pdb.set_trace()
    # for ww3_cur_path in array_to_process:
    #     year = ww3_cur_path.split('/')[-1].split('.')[1]
    #     cur_experiment = ww3_cur_path.split('/')[-1].split('.')[0]
    # 
    #     print '\n Ploting year %s from experiment %s \n\n' % (year, cur_experiment)
    # 
    #     ww3_no_cur_path = 'results/netcdf_files/ww3_nocur.%s.nc' % (year) 
    # 
    #     plot_instance = PlotResults(ww3_cur_path, ww3_no_cur_path)
    #     plot_instance.make_video_regional()
    
    # Rio -43.472722, -23.102309
    # Maresias -45.596076, -23.825660
    # Guaruja -46.230839, -24.021979
    