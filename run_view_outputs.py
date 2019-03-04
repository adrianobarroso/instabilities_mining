import yaml
import xray
from matplotlib import pyplot as plt
from plot_results import *

if __name__ == "__main__":
    array_to_process = [
        # [xdataset_url_2013b  , ydataset_url_2013b],
        # [xdataset_url_2014a , ydataset_url_2014a],
        # [xdataset_url_2014b , ydataset_url_2014b],
        # [xdataset_url_2015  , ydataset_url_2015],
        # [xdataset_url_2016  , ydataset_url_2016]
    ]
    
    ww3_cur = xray.open_dataset('results/netcdf_files/ww3_hycom.2016.nc')
    # ww3_cur = xray.open_dataset('results/netcdf_files/ww3_hycom.2014_ef.nc')
    # ww3_cur = xray.open_dataset('results/netcdf_files/ww3_mercator.2014.nc')
    
    ww3_no_cur = xray.open_dataset('results/netcdf_files/ww3_nocur.2016.nc')
    # ww3_no_cur = xray.open_dataset('results/netcdf_files/ww3_nocur.2014_ef.nc')
    
    pnboia = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Bcabo_frio2.nc')
    # pnboia = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Bsantos2.nc') # 2017
    # pnboia = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Bsantos.nc')
    # pnboia = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Bguanabara2.nc') # 2017
    # pnboia = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Bguanabara.nc')
    # pnboia = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Bsanta_catarina2.nc') # 2017
    # pnboia = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Brio_grande2.nc') # 2017
    # pnboia = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Brio_grande.nc')
    
    # import pdb; pdb.set_trace()
    
    plot_instance = PlotResults(ww3_cur, ww3_no_cur, pnboia)
    
    # Rio -43.472722, -23.102309
    # Maresias -45.596076, -23.825660
    # Guaruja -46.230839, -24.021979
    
    # plot_instance.hs_comparison(-46.230839, -24.021979)
    plot_instance.hs_comparison_pnboia()
    
    # plot_instance.hs_comparison(-42, -24)
    # import pdb; pdb.set_trace()
   
        
            
