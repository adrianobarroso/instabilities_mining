import os
from tool_scripts import *
from hycom_dataset import *

if __name__ == "__main__":
    
    xdataset_url_2016 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.2/2016/uvel'
    ydataset_url_2016 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.2/2016/vvel'
    
    #wget_u = 'ftp://ftp.hycom.org//datasets/GLBa0.08/expt_91.1/2016/uvel/archv.2016_007_00_3zu.nc'
    wget_url = 'ftp://ftp.hycom.org/datasets/GLBa0.08/expt_91.2/2016/2d/archv.2016_109_00_2d.nc'
    
    os.system('wget %s' % (wget_url))
    
    run = [xdataset_url_2016, ydataset_url_2016]
    
    data_stations = get_yaml('dataset/buoys_stations.yml')
    [array_lon, array_lat] = array_stations(data_stations)
    
    dataset_instance = HycomDataSet(run[0], run[1])
    dataset_instance.print_datasets()

    minlat = np.array(array_lat).min() - 3
    maxlat = np.array(array_lat).max() + 3
    minlon = np.array(array_lon).min() - 3
    maxlon = np.array(array_lon).max() + 3

    [_l, i1] = find_nearest_value_index(dataset_instance.lon_array, np.round(minlon))
    [_l, i2] = find_nearest_value_index(dataset_instance.lon_array, np.round(maxlon))
    
    [_l, j1] = find_nearest_value_index(dataset_instance.lat_array, np.round(minlat))
    [_l, j2] = find_nearest_value_index(dataset_instance.lat_array, np.round(maxlat))

    dataset_instance.download(i1, i2, j1, j2)
