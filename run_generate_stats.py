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
        [xdataset_url_2013  , ydataset_url_2013],
        [xdataset_url_2014a , ydataset_url_2014a],
        [xdataset_url_2014b , ydataset_url_2014b],
        [xdataset_url_2015  , ydataset_url_2015],
        [xdataset_url_2016  , ydataset_url_2016]
    ]
    # array_to_process = [
    #     [xdataset_url_2013  , ydataset_url_2013]
    #     # [xdataset_url_2014a , ydataset_url_2014a],
    #     # [xdataset_url_2014b , ydataset_url_2014b],
    #     # [xdataset_url_2015  , ydataset_url_2015],
    #     # [xdataset_url_2016  , ydataset_url_2016]
    # ]
    
    for run in array_to_process:
        print('Running prints of run %s' % run[0])
        dataset_instance = HycomDataSet(run[0], run[1])
        dataset_instance.print_datasets()
        # Plot(dataset_instance).plot_uv_series(-42, -24)
        Plot(dataset_instance).plot_gradient_series(-42, -24)
    
    # Plot(dataset_instance).plot_area_buoy()
    # Plot(dataset_instance).plot_uv_series(-45, -23, 'vvel')
    # 
    # y_dataset_instance = HycomDataSet(ydataset_url_2014)
    # y_dataset_instance.print_dataset()
    
    # Plot(y_dataset_instance).plot_v_series(-45, -23)
    # Plot(x_dataset_instance).plot_gradient_series(-45, -23)
    
    