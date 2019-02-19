import os
from tool_scripts import *
import yaml
from hycom_dataset import *

if __name__ == "__main__":
    os.system('mkdir -p netcdf_files')

    dataset_url_2013a = '%s/%s/%s/%svel?var=%s&north=-18&west=-55&east=-38&south=-36&disableProjSubset=on&horizStride=1&time_start=%s&time_end=%s&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf' % (
        'http://ncss.hycom.org/thredds/ncss/GLBa0.08',
        'expt_90.9',
        '2013',
        '__var__',
        '__var__',
        '2013-01-01T00:00:00Z',
        '2013-08-20T00:00:00Z'
    )

    # import pdb; pdb.set_trace();
    dataset_url_2013b = '%s/%s/%s/%svel?var=%s&north=-18&west=-55&east=-38&south=-36&disableProjSubset=on&horizStride=1&time_start=%s&time_end=%s&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf' % (
        'http://ncss.hycom.org/thredds/ncss/GLBa0.08',
        'expt_91.0',
        '2013b',
        '__var__',
        '__var__',
        '2013-08-21T00:00:00Z',
        '2013-12-31T00:00:00Z'
    )

    dataset_url_2014a = '%s/%s/%s/%svel?var=%s&north=-18&west=-55&east=-38&south=-36&disableProjSubset=on&horizStride=1&time_start=%s&time_end=%s&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf' % (
        'http://ncss.hycom.org/thredds/ncss/GLBa0.08',
        'expt_91.0',
        '2014',
        '__var__',
        '__var__',
        '2014-01-01T00:00:00Z',
        '2014-04-04T00:00:00Z'
    )

    dataset_url_2014b = '%s/%s/%s/%svel?var=%s&north=-18&west=-55&east=-38&south=-36&disableProjSubset=on&horizStride=1&time_start=%s&time_end=%s&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf' % (
        'http://ncss.hycom.org/thredds/ncss/GLBa0.08',
        'expt_91.1',
        '2014',
        '__var__',
        '__var__',
        '2014-04-05T00:00:00Z',
        '2014-12-31T00:00:00Z'
    )

    dataset_url_2015 = '%s/%s/%s/%svel?var=%s&north=-18&west=-55&east=-38&south=-36&disableProjSubset=on&horizStride=1&time_start=%s&time_end=%s&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf' % (
        'http://ncss.hycom.org/thredds/ncss/GLBa0.08',
        'expt_91.1',
        '2015',
        '__var__',
        '__var__',
        '2015-01-01T00:00:00Z',
        '2015-12-31T00:00:00Z'
    )

    dataset_url_2016 = '%s/%s/%s/%svel?var=%s&north=-18&west=-55&east=-38&south=-36&disableProjSubset=on&horizStride=1&time_start=%s&time_end=%s&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf' % (
        'http://ncss.hycom.org/thredds/ncss/GLBa0.08',
        'expt_91.2',
        '2016',
        '__var__',
        '__var__',
        '2016-04-18T00:00:00Z',
        '2016-12-31T00:00:00Z'
    )

    dataset_to_process = {
        'dataset_url_2013a': dataset_url_2013a,
        'dataset_url_2013b': dataset_url_2013b,
        'dataset_url_2014a': dataset_url_2014a,
        'dataset_url_2014b': dataset_url_2014b,
        'dataset_url_2015': dataset_url_2015,
        'dataset_url_2016': dataset_url_2016
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