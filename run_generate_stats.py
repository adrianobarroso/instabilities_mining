import yaml
from hycom_dataset import *

if __name__ == "__main__":
    # xdataset_url_2008 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/uvel'
    # ydataset_url_2008 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/vvel'
    xdataset_url_2013 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.0/2013/uvel'
    ydataset_url_2013 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.0/2013/vvel'

    xdataset_url_2014a = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.0/2014/uvel'
    ydataset_url_2014a = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.0/2014/vvel'

    xdataset_url_2014b = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2014/uvel'
    ydataset_url_2014b = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2014/vvel'

    xdataset_url_2015 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2015/uvel'
    ydataset_url_2015 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2015/vvel'

    xdataset_url_2016 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.2/2016/uvel'
    ydataset_url_2016 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.2/2016/vvel'

    array_to_process = [
        # [xdataset_url_2013  , ydataset_url_2013],
        # [xdataset_url_2014a , ydataset_url_2014a],
        # [xdataset_url_2014b , ydataset_url_2014b],
#        [xdataset_url_2015  , ydataset_url_2015],
        [xdataset_url_2016  , ydataset_url_2016]
    ]

    for run in array_to_process:
        print('Running prints of run %s' % run[0])

        dataset_instance = HycomDataSet(run[0], run[1])
        dataset_instance.print_datasets()

        plot_instance = Plot(dataset_instance)
        data_stations = get_yaml('dataset/buoys_stations.yml')
        [array_lon, array_lat] = array_stations(data_stations)

        [_lon, ix] = find_nearest_value_index(dataset_instance.lon_array, -42)
        [_lat, iy] = find_nearest_value_index(dataset_instance.lat_array, -24)

        useries = dataset_instance.ydataset_persist.v.isel(X=ix, Y=iy, Depth=0)
        vseries = dataset_instance.xdataset_persist.u.isel(X=ix, Y=iy, Depth=0)

        for mt_index in range(useries.MT.size):
            [run, exp, year] = dataset_instance.xdataset_url.split('/')[-4:-1]
            print('\n\n\n')
            print('Plotting map for dataset %s experiment %s year %s \n Date: %s MT: %s' % (
                    run,
                    exp,
                    year,
                    str(useries[mt_index].Date.values), 
                    str(useries[mt_index].MT.values)
                )
            )

            import pdb; pdb.set_trace();           
            plot_instance.quiver_plot(mt_index, [0, 1.2])

        # for project in data_stations:
        #     for station in data_stations[project]:
        #         lon = data_stations[project][station]['lon']
        #         lat = data_stations[project][station]['lat']
        # 
        #         [_lon, ix] = find_nearest_value_index(dataset_instance.lon_array, lon)
        #         [_lat, iy] = find_nearest_value_index(dataset_instance.lat_array, lat)
        # 
        #         useries = dataset_instance.ydataset_persist.v.isel(X=ix, Y=iy, Depth=0)
        #         vseries = dataset_instance.xdataset_persist.u.isel(X=ix, Y=iy, Depth=0)
        # 
        #         index_high_useries_gradient_mt = np.where(np.gradient(useries) > 0.2)
        #         index_high_vseries_gradient_mt = np.where(np.gradient(vseries) > 0.2)
        # 
        #         if (index_high_vseries_gradient_mt[0].size > index_high_useries_gradient_mt[0].size):
        #             used_index = index_high_vseries_gradient_mt[0]
        #         else:
        #             used_index = index_high_useries_gradient_mt[0]
        # 
        #         for mt_index in used_index:
        #             [run, exp, year] = dataset_instance.xdataset_url.split('/')[-4:-1]
        #             print('\n\n\n')
        #             print('Plotting map for dataset %s experiment %s year %s \n Date: %s MT: %s' % (
        #                     run,
        #                     exp,
        #                     year,
        #                     str(useries[mt_index].Date.values), 
        #                     str(useries[mt_index].MT.values)
        #                 )
        #             )
        # 
        #             plot_instance.quiver_plot(mt_index, [0, 1.2])
                    
                # import pdb; pdb.set_trace();
                
                # Ploting series
                # plot_instance.plot_uv_series(lon, lat)
                # plot_instance.plot_gradient_series(lon, lat)

