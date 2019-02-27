import os
from tool_scripts import *
import yaml
from hycom_dataset import *
from datasets import *

if __name__ == "__main__":
    subsetdir = 'netcdf_files/subset'
    os.system('mkdir -p %s' % (subsetdir))
    
    dataset_to_process = {
        'dataset_url_2013a': DATASET_URL_2013a,
        'dataset_url_2013b': DATASET_URL_2013b,
        'dataset_url_2014a': DATASET_URL_2014a,
        'dataset_url_2014b': DATASET_URL_2014b,
        'dataset_url_2015': DATASET_URL_2015,
        'dataset_url_2016': DATASET_URL_2016
    }
    
    for dataset in dataset_to_process:
        splitted_url = dataset_to_process[dataset].split("__var__")
        dimensions = ['u', 'v']
        
        for dimension in dimensions:
            # import pdb; pdb.set_trace()
            netcdf_file = 'netcdf_files/%svel_%s.nc' % (dimension, dataset.split('_')[-1])
            netcdf_output = '%s/%svel_%s_nodepth.nc' % (subsetdir, dimension, dataset.split('_')[-1])
            
            os.system('ncwa -O -a Depth %s %s' % (netcdf_file, netcdf_output))
            os.system('ncks -O -C -x -v Depth %s %s' % (netcdf_output, netcdf_output))
    
            # import pdb; pdb.set_trace()
            os.system('ncrename -O -v Latitude,latitude %s %s' % (netcdf_output, netcdf_output))
            os.system('ncrename -O -v Longitude,longitude %s %s' % (netcdf_output, netcdf_output))
            os.system('ncrename -O -v %s,%scur %s %s' % (dimension, dimension, netcdf_output, netcdf_output))
    