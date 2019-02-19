import os
from tool_scripts import *
import yaml
from hycom_dataset import *
from datasets import *

if __name__ == "__main__":
    os.system('mkdir -p netcdf_files')

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
            url = splitted_url[0] + dimension + splitted_url[1] + dimension + splitted_url[2]
            print '\n\n'
            print url            
            # import pdb; pdb.set_trace()
            os.system('wget -O netcdf_files/%svel_%s.nc \'%s\'' % (dimension, dataset.split('_')[-1], url))