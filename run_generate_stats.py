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
        [xdataset_url_2015  , ydataset_url_2015],
        [xdataset_url_2016  , ydataset_url_2016]
    ]

    for run in array_to_process:
        print('Running prints of run %s' % run[0])

        dataset_instance = HycomDataSet(run[0], run[1])
        dataset_instance.print_datasets()

        plot_instance = Plot(dataset_instance)
        data_stations = plot_instance.get_yaml('dataset/buoys_stations.yml')
        [array_lon, array_lat] = array_stations(data_stations)

        for project in data_stations:
            for station in data_stations[project]:
                lon = data_stations[project][station]['lon']
                lat = data_stations[project][station]['lat']

                plot_instance.quiver_plot()

                # plot_instance.plot_uv_series(lon, lat)
                # plot_instance.plot_gradient_series(lon, lat)

        # Plot(dataset_instance).plot_uv_series(-42, -24)
        # plot_instance.array_stations(self, data_stations)

        # plot.plot_gradient_series(-42, -24)

    # Plot(dataset_instance).plot_area_buoy()
    # Plot(dataset_instance).plot_uv_series(-45, -23, 'vvel')
    #
    # y_dataset_instance = HycomDataSet(ydataset_url_2014)
    # y_dataset_instance.print_dataset()

    # Plot(y_dataset_instance).plot_v_series(-45, -23)
    # Plot(x_dataset_instance).plot_gradient_series(-45, -23)
