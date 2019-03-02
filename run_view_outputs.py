import yaml
import xray
from matplotlib import pyplot as plt

if __name__ == "__main__":
    array_to_process = [
        # [xdataset_url_2013b  , ydataset_url_2013b],
        # [xdataset_url_2014a , ydataset_url_2014a],
        # [xdataset_url_2014b , ydataset_url_2014b],
        # [xdataset_url_2015  , ydataset_url_2015],
        # [xdataset_url_2016  , ydataset_url_2016]
    ]
    
    ww3_hycom_cur = xray.open_dataset('/Users/adriano/Oceano/COPPE/Masters/instabilities_mining/results/ww3_hycom.2014.nc')
    ww3_no_cur = xray.open_dataset('/Users/adriano/Oceano/COPPE/Masters/instabilities_mining/results/ww3_nocur.2014.nc')
    import pdb; pdb.set_trace();
   
        
            
