import yaml
from hycom_dataset import *
from datasets import *

if __name__ == "__main__":
    dataset_to_process = {
        'dataset_url_2013a': DATASET_URL_2013a,
        # 'dataset_url_2013b': DATASET_URL_2013b,
        # 'dataset_url_2014a': DATASET_URL_2014a,
        # 'dataset_url_2014b': DATASET_URL_2014b,
        # 'dataset_url_2015': DATASET_URL_2015,
        # 'dataset_url_2016': DATASET_URL_2016
    }

    for dataset in dataset_to_process:
        # for dimension in dimensions:
        print '\n\n'

        # import pdb; pdb.set_trace()
        u_netcdf_output = 'netcdf_files/uvel_%s.nc' % (dataset.split('_')[-1])
        v_netcdf_output = 'netcdf_files/vvel_%s.nc' % (dataset.split('_')[-1])
        
        print u_netcdf_output
        file_size = os.path.getsize(u_netcdf_output)
        
        if file_size > 10777616:
    
            dataset_instance = HycomDataSet(u_netcdf_output, v_netcdf_output)
            dataset_instance.print_datasets()

            plot_instance = Plot(dataset_instance)
            
            data_stations = get_yaml('dataset/buoys_stations.yml')
            [array_lon, array_lat] = array_stations(data_stations)
            
            gradient_index = []
            gradient_indexes_with_lon_lat = []
            lon_lat_index_dicts = {}
            for project in data_stations:
                for station in data_stations[project]:
                    lon = data_stations[project][station]['lon']
                    lat = data_stations[project][station]['lat']
                    
                    [_lon, ix] = find_nearest_value_index(dataset_instance.lon_array, lon)
                    [_lat, iy] = find_nearest_value_index(dataset_instance.lat_array, lat)
                    
                    # import pdb; pdb.set_trace();
                    
                    gradient_limit = 0.3
                    used_index = dataset_instance.high_gradient_uv_series_index(ix, iy, gradient_limit)
                    
                    gradient_index = np.append(gradient_index, used_index)                
                    # # import pdb; pdb.set_trace();
                    gradient_index_with_lon_lat = [gradient_index, _lon, _lat]
                    #                    
                    gradient_indexes_with_lon_lat.append(gradient_index_with_lon_lat)
                    # 
                    all_gradient_mt_index = np.unique(gradient_index)
                    # dicts[str(_lon) + '_' + str(_lat)] = all_gradient_mt_index
                    for ii in all_gradient_mt_index:
                        if str(int(ii)) in lon_lat_index_dicts:
                            lon_lat_index_dicts[str(int(ii))] += [[_lon, _lat]]
                        else:
                            lon_lat_index_dicts[str(int(ii))] = [[_lon, _lat]]
                        
        # 
        # import pdb; pdb.set_trace();
        for index in all_gradient_mt_index:
            dataset_instance.set_time_series_coordinate()
            # import pdb; pdb.set_trace();
            # [run, exp, year] = dataset_instance.xdataset_url.split('/')[-4:-1]
            year = dataset_instance.xdataset_url.split('_')[-1].split('.')[0]
            
            print('\n\n')
            print('Plotting map for dataset year %s \n Date: %s MT: %s' % (
                    year,
                    str(dataset_instance.time_range[int(index)].strftime("%Y/%m/%d")), 
                    str(dataset_instance.xdataset_persist.MT[int(index)].values)
                )
            )
        # 
            plot_instance.quiver_plot_around_instability(int(index), lon_lat_index_dicts, [0, 1.2])
        #     # import pdb; pdb.set_trace();
        # 
        #     date_quiver = dataset_instance.xdataset_persist.u.Date[int(index)].values
        #     fig_dir = '%s/%s' % ('images/mapas/instabilities', int(date_quiver))
        # 
        #     cmd = "ffmpeg -y -r 1 -pattern_type glob -i '%s/*.jpg' -c:v libx264 mapa_%s.mp4" % (fig_dir, int(date_quiver))
        #     os.system(cmd)
        # 
        #     # cmd = 'convert -delay 60 -loop 0 %s/mapa_ano_%s* mapa_%s_%s.gif' % (fig_dir, year, year, int(date_quiver)) 
        #     # import pdb; pdb.set_trace()
        #     # gif_name = '%s/mapa_ano_%s_index_%s_.jpg' % (fig_dir, int(date_quiver), int(dataset_instance.xdataset_persist.u.MT[int(index)].values))
        # 
        # 