import os
from tool_scripts import *
import yaml
from hycom_dataset import *

if __name__ == "__main__":
    os.system('mkdir -p netcdf_files')
    # http://ncss.hycom.org/thredds/ncss/GLBa0.08/expt_91.2/2017/uvel?var=u&north=-10&west=220&east=250&south=-33&disableProjSubset=on&horizStride=1&time_start=2017-01-01T00%3A00%3A00Z&time_end=2017-12-31T00%3A00%3A00Z&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf

    # xdataset_url_2013a = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.9/2013/uvel'
    dataset_url_2013a = '%s/%s/%s/uvel?var=u&north=-18&west=-55&east=-38&south=-36&disableProjSubset=on&horizStride=1&time_start=%s&time_end=%s&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf' % (
        'http://ncss.hycom.org/thredds/ncss/GLBa0.08',
        'expt_90.9',
        '2013',
        '2013-01-01T00:00:00Z',
        '2013-08-20T00:00:00Z'
    )

    os.system('wget -O netcdf_files/uvel_%s.nc \'%s\'' % ('2013a', xdataset_url_2013a))
    os.system('wget -O netcdf_files/vvel_%s.nc \'%s\'' % ('2013a', ydataset_url_2013a))

    # import pdb; pdb.set_trace();
    # http://ncss.hycom.org/thredds/ncss/GLBa0.08/expt_90.9/2013/uvel/dataset.html
    # http://ncss.hycom.org/thredds/ncss/GLBa0.08/expt_90.9/2013/vvel/dataset.html

    # xdataset_url_2013b = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.0/2013/uvel'
    # ydataset_url_2013b = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.0/2013/vvel'
    dataset_url_2013b = '%s/%s/%s/vvel?var=v&north=-18&west=-55&east=-38&south=-36&disableProjSubset=on&horizStride=1&time_start=%s&time_end=%s&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf' % (
        'http://ncss.hycom.org/thredds/ncss/GLBa0.08',
        'expt_91.0',
        '2013b',
        '2013-08-21T00:00:00Z',
        '2013-12-31T00:00:00Z'
    )

    # http://ncss.hycom.org/thredds/ncss/GLBa0.08/expt_91.0/2014/vvel/dataset.html
    # xdataset_url_2014a = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.0/2014/uvel'
    # ydataset_url_2014a = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.0/2014/vvel'
    dataset_url_2014a = '%s/%s/%s/vvel?var=v&north=-18&west=-55&east=-38&south=-36&disableProjSubset=on&horizStride=1&time_start=%s&time_end=%s&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf' % (
        'http://ncss.hycom.org/thredds/ncss/GLBa0.08',
        'expt_91.0',
        '2014',
        '2014-01-01T00:00:00Z',
        '2014-04-04T00:00:00Z'
    )

    # xdataset_url_2014b = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2014/uvel'
    # ydataset_url_2014b = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2014/vvel'
    dataset_url_2014b = '%s/%s/%s/vvel?var=v&north=-18&west=-55&east=-38&south=-36&disableProjSubset=on&horizStride=1&time_start=%s&time_end=%s&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf' % (
        'http://ncss.hycom.org/thredds/ncss/GLBa0.08',
        'expt_91.1',
        '2014',
        '2014-04-05T00:00:00Z',
        '2014-12-31T00:00:00Z'
    )

    # xdataset_url_2015 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2015/uvel'
    # ydataset_url_2015 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2015/vvel'
    dataset_url_2015 = '%s/%s/%s/vvel?var=v&north=-18&west=-55&east=-38&south=-36&disableProjSubset=on&horizStride=1&time_start=%s&time_end=%s&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf' % (
        'http://ncss.hycom.org/thredds/ncss/GLBa0.08',
        'expt_91.1',
        '2015',
        '2015-01-01T00:00:00Z',
        '2015-12-31T00:00:00Z'
    )

    # xdataset_url_2016 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.2/2016/uvel'
    # ydataset_url_2016 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.2/2016/vvel'
    dataset_url_2016 = '%s/%s/%s/%svel?var=%s&north=-18&west=-55&east=-38&south=-36&disableProjSubset=on&horizStride=1&time_start=%s&time_end=%s&timeStride=1&vertCoord=0&addLatLon=true&accept=netcdf' % (
        'http://ncss.hycom.org/thredds/ncss/GLBa0.08',
        'expt_91.2',
        '2016',
        '',
        '',
        '2016-04-18T00:00:00Z',
        '2016-12-31T00:00:00Z'
    )

    array_to_process = [
        [xdataset_url_2013a  , ydataset_url_2013a],
        # [xdataset_url_2013b  , ydataset_url_2013b],
        # [xdataset_url_2014a , ydataset_url_2014a],
        # [xdataset_url_2014b , ydataset_url_2014b],
        # [xdataset_url_2015  , ydataset_url_2015],
        # [xdataset_url_2016  , ydataset_url_2016]
    ]

    # os.system('wget %s' % (wget_url))
    #
    # run = [xdataset_url_2016, ydataset_url_2016]
    #
    # data_stations = get_yaml('dataset/buoys_stations.yml')
    # [array_lon, array_lat] = array_stations(data_stations)
    #
    # dataset_instance = HycomDataSet(run[0], run[1])
    # dataset_instance.print_datasets()
    #
    # minlat = np.array(array_lat).min() - 3
    # maxlat = np.array(array_lat).max() + 3
    # minlon = np.array(array_lon).min() - 3
    # maxlon = np.array(array_lon).max() + 3
    #
    # [_l, i1] = find_nearest_value_index(dataset_instance.lon_array, np.round(minlon))
    # [_l, i2] = find_nearest_value_index(dataset_instance.lon_array, np.round(maxlon))
    #
    # [_l, j1] = find_nearest_value_index(dataset_instance.lat_array, np.round(minlat))
    # [_l, j2] = find_nearest_value_index(dataset_instance.lat_array, np.round(maxlat))
    #
    # dataset_instance.download(i1, i2, j1, j2)
