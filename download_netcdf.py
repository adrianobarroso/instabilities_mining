import os
from tool_scripts import *
import yaml
from hycom_dataset import *

if __name__ == "__main__":
    # http://ncss.hycom.org/thredds/ncss/GLBa0.08/expt_91.2/2017/uvel?var=u&north=-10&west=220&east=250&south=-33&disableProjSubset=on&horizStride=1&time_start=2017-01-01T00%3A00%3A00Z&time_end=2017-12-31T00%3A00%3A00Z&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf
    
    # http://ncss.hycom.org/thredds/ncss/GLBa0.08/expt_91.2/2017/uvel/dataset.html
    # http://ncss.hycom.org/thredds/ncss/GLBa0.08/expt_91.2/2017/vvel/dataset.html
    # 'http://ncss.hycom.org/thredds/ncss/GLBa0.08/expt_91.2/2017/uvel?var=u&north=-20&west=-53&east=-40&south=-35&horizStride=1&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf'
    # xdataset_url_2008 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/uvel'
    # ydataset_url_2008 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/vvel'
    xdataset_url_2013a = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.9/2013/uvel'
    ydataset_url_2013a = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.9/2013/vvel'
    url = '%s/%s/%s/uvel?var=u&north=-20&west=-53&east=-40&south=-35&disableProjSubset=on&horizStride=1&time_start=%s&time_end=%s&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf' % (
        'http://ncss.hycom.org/thredds/ncss/GLBa0.08',
        'expt_90.9',
        '2013',
        '2013-01-01T00:00:00Z',
        '2013-08-20T00:00:00Z'
    )
    
    import pdb; pdb.set_trace()
    
    os.system('wget -O uvel.nc %s' % (url))
    
    # http://ncss.hycom.org/thredds/ncss/GLBa0.08/expt_90.9/2013/uvel/dataset.html
    # http://ncss.hycom.org/thredds/ncss/GLBa0.08/expt_90.9/2013/vvel/dataset.html
    
    xdataset_url_2013b = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.0/2013/uvel'
    ydataset_url_2013b = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.0/2013/vvel'

    xdataset_url_2014a = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.0/2014/uvel'
    ydataset_url_2014a = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.0/2014/vvel'

    xdataset_url_2014b = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2014/uvel'
    ydataset_url_2014b = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2014/vvel'

    xdataset_url_2015 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2015/uvel'
    ydataset_url_2015 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2015/vvel'

    xdataset_url_2016 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.2/2016/uvel'
    ydataset_url_2016 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.2/2016/vvel'

    array_to_process = [
        [xdataset_url_2013a  , ydataset_url_2013a],
        # [xdataset_url_2013b  , ydataset_url_2013b],
        # [xdataset_url_2014a , ydataset_url_2014a],
        # [xdataset_url_2014b , ydataset_url_2014b],
        # [xdataset_url_2015  , ydataset_url_2015],
        # [xdataset_url_2016  , ydataset_url_2016]
    ]        
    xdataset_url_2016 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.2/2016/uvel'
    ydataset_url_2016 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.2/2016/vvel'
    
    #wget_u = 'ftp://ftp.hycom.org//datasets/GLBa0.08/expt_91.1/2016/uvel/archv.2016_007_00_3zu.nc'
    # wget_url = 'ftp://ftp.hycom.org/datasets/GLBa0.08/expt_91.2/2016/2d/archv.2016_109_00_2d.nc'
    
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
