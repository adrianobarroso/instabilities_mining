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
    
     # xray.open_dataset('https://data.nodc.noaa.gov/thredds/dodsC/ncep/rtofs/2015/201501/ofs.20150131/surface/ofs_atl.t00z.f010.20150131.grb.grib2')

    for run in array_to_process:        
        print('Running prints of run %s' % run[0])

        dataset_instance = HycomDataSet(run[0], run[1])
        dataset_instance.print_datasets()

        plot_instance = Plot(dataset_instance)
        data_stations = get_yaml('dataset/buoys_stations.yml')
        [array_lon, array_lat] = array_stations(data_stations)
        
        gradient_index = []
        gradient_indexes_with_lon_lat = []
        for project in data_stations:
            for station in data_stations[project]:
                lon = data_stations[project][station]['lon']
                lat = data_stations[project][station]['lat']
        
                [_lon, ix] = find_nearest_value_index(dataset_instance.lon_array, lon)
                [_lat, iy] = find_nearest_value_index(dataset_instance.lat_array, lat)
        
                gradient_limit = 0.35
                used_index = dataset_instance.high_gradient_uv_series_index(ix, iy, gradient_limit)
                
                gradient_index = np.append(gradient_index, used_index)                
                # import pdb; pdb.set_trace();
                gradient_index_with_lon_lat = [gradient_index, _lon, _lat]
                
                gradient_indexes_with_lon_lat.append(gradient_index_with_lon_lat)
                
        all_gradient_mt_index = np.unique(gradient_index)

        import pdb; pdb.set_trace();
        for index in [all_gradient_mt_index[-1]]:
            [run, exp, year] = dataset_instance.xdataset_url.split('/')[-4:-1]
            # import pdb; pdb.set_trace();
            print('\n\n')
            print('Plotting map for dataset %s experiment %s year %s \n Date: %s MT: %s' % (
                    run,
                    exp,
                    year,
                    str(dataset_instance.xdataset_persist.Date[int(index)].values), 
                    str(dataset_instance.xdataset_persist.Date[int(index)].MT.values)
                )
            )
            
            plot_instance.quiver_plot_around_instability(int(index), [0, 1.2])
            # import pdb; pdb.set_trace();
            
            date_quiver = dataset_instance.xdataset_persist.u.Date[int(index)].values
            fig_dir = '%s/%s' % ('images/mapas/instabilities', int(date_quiver))
            
            cmd = "ffmpeg -y -r 1 -pattern_type glob -i '%s/*.jpg' -c:v libx264 mapa_%s.mp4" % (fig_dir, int(date_quiver))
            os.system(cmd)
            
            # cmd = 'convert -delay 60 -loop 0 %s/mapa_ano_%s* mapa_%s_%s.gif' % (fig_dir, year, year, int(date_quiver)) 
            # import pdb; pdb.set_trace()
            # gif_name = '%s/mapa_ano_%s_index_%s_.jpg' % (fig_dir, int(date_quiver), int(dataset_instance.xdataset_persist.u.MT[int(index)].values))
            
            