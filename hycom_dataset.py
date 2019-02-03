import xray
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from plot_scripts import *

class HycomDataSet:
    # Initializer / Instance Attributes
    def __init__(self, xdataset_url, ydataset_url):
        self.xdataset_url = xdataset_url
        self.ydataset_url = ydataset_url
        self.load_dataset()

    def set_lon_lat_array_coordinates(self):
        lon_array = self.xdataset_persist.Longitude[0, :].values
        
        self.lon_array = lon_array - lon_array[0] - 180
        self.lat_array = self.xdataset_persist.Latitude[:, 0].values
    
    def set_time_series_coordinate(self):
        mt = self.xdataset_persist.MT
        
        date = datetime.datetime(1900, 12, 31, 0, 0, 0)
        start_date = date + datetime.timedelta(days=mt.values[0])
        end_date = date + datetime.timedelta(days=mt.values[-1])
        
        self.time_range = pd.date_range(start_date, end_date)

    def print_datasets(self):
        print(self.xdataset_persist)
        print(self.ydataset_persist)
  
    # def dataset(self):
    #     self.xdataset_persist = self.xdataset_persist or self.load_dataset()
    #     self.set_lon_lat_array_coordinates()
    #     self.set_time_series_coordinate()
    # 
    #     return self.xdataset_persist
    
    def load_dataset(self):
        self.xdataset_persist = xray.open_dataset(self.xdataset_url, decode_times=False)
        self.ydataset_persist = xray.open_dataset(self.ydataset_url, decode_times=False)
        self.set_lon_lat_array_coordinates()
        self.set_time_series_coordinate()
        
class Plot:
    def __init__(self, hycom_object):
        self.hycom_object = hycom_object
        
    def plot_area_buoy(self):
        from mpl_toolkits.basemap import Basemap
        import yaml
        
        buoy_station_file='dataset/buoys_stations.yml'
        file = open(buoy_station_file).read()
        data_stations = yaml.load(file)

        [array_lon, array_lat] = array_stations(self, data_stations)

        minlat = np.array(array_lat).min()
        maxlat = np.array(array_lat).max()
        minlon = np.array(array_lon).min()
        maxlon = np.array(array_lon).max()
        
        central_lat = (minlat + maxlat)/2
        central_lon = (minlon + maxlon)/2    
        
        # setup Lambert Conformal basemap.
        m = Basemap(width=4000000,height=3000000,projection='lcc',
                    resolution='l',lat_1=minlat,lat_2=maxlat,lat_0=central_lat,lon_0=central_lon)
        # draw coastlines.
        m.drawcoastlines()
        m.bluemarble()
        x, y = m(array_lon, array_lat)
        m.scatter(x, y, 30, marker='o', color='red', zorder=100)
        m.drawparallels(np.arange(m.llcrnrlat,m.urcrnrlat,5.), labels=[0,1,0,0], color='white', dashes=[1, 4])
        m.drawmeridians(np.arange(m.llcrnrlon,m.urcrnrlon,10.), labels=[0,0,0,1], color='white', dashes=[1, 4])
        
        for project in data_stations:
            for station in data_stations[project]:
                lon = data_stations[project][station]['lon']
                lat = data_stations[project][station]['lat']
                plt.annotate('Barcelona', xy=(m.urcrnrlon, m.llcrnrlat),  xycoords='data',
                                xytext=(lon, lat), textcoords='offset points',
                                color='r',
                                arrowprops=dict(arrowstyle="fancy", color='g')
                                )
        # draw a boundary around the map, fill the background.
        # this background will end up being the ocean color, since
        # the continents will be drawn on top.
        m.drawmapboundary()
        # fill continents, set lake color same as ocean color.
        # m.fillcontinents(color='black',lake_color='aqua')
        import pdb; pdb.set_trace()
        # plt.show()
        
    def plot_uv_series(self, lon, lat, component):        
        ix = find_nearest_value_index(self.hycom_object.lon_array, lon)
        iy = find_nearest_value_index(self.hycom_object.lat_array, lat)
        # fig_name = 'HYCOM_' + '_'.join(self.hycom_object.dataset_url.split('/')[-4:-3]) + '_' + component + '_' + self.hycom_object.dataset_url.split('/')[-2] + '.jpg'
        # import pdb; pdb.set_trace()
        [run, exp, year] = self.hycom_object.xdataset_url.split('/')[-4:-1]
        
        fig_name = 'HYCOM_%s_%s_%s_%s.jpg' % (run, exp, component, year)
        
        if component == 'vvel':
            series = self.hycom_object.ydataset_persist.v.isel(X=ix[1], Y=iy[1], Depth=0)
        else:
            series = self.hycom_object.xdataset_persist.u.isel(X=ix[1], Y=iy[1], Depth=0)
            
        # import pdb; pdb.set_trace()
        fig = plt.figure()
        series.plot()
        
        plt.xlabel('time in year ' + year)
        plt.ylabel(component + ' (m/s)')
        fig.savefig('images/' + fig_name)
        
    def plot_gradient_series(self, lon, lat):
        ix = find_nearest_value_index(self.hycom_object.lon_array, lon)
        iy = find_nearest_value_index(self.hycom_object.lat_array, lat)
        
        if self.hycom_object.dataset_url.split('/')[-1] == 'vvel':
            serie = self.hycom_object.xdataset_persist.v.isel(X=ix[1], Y=iy[1], Depth=0).values
        else:
            serie = self.hycom_object.xdataset_persist.u.isel(X=ix[1], Y=iy[1], Depth=0).values
        
        fig = plt.figure()
        plt.plot(self.hycom_object.xdataset_persist.MT.values, np.gradient(serie))
        plt.title('Lon=' + str(lon) + ' Lat=' + str(lat))
        plt.xlabel('time in year ' + self.hycom_object.dataset_url.split('/')[-2])
        plt.ylabel(self.hycom_object.dataset_url.split('/')[-1] + ' gradient')
        
        fig_name = 'HYCOM_gradient_series' + '_'.join(self.hycom_object.dataset_url.split('/')[-4:]) + '_lon_' + str(lon) + '_lat_' + str(lat) + '.jpg'
        fig.savefig('images/' + fig_name)

if __name__ == "__main__":
        
    xdataset_url_2008 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/uvel'
    ydataset_url_2008 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/vvel'
    
    xdataset_url_2014 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2014/uvel'
    ydataset_url_2014 = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2014/vvel'

    dataset_instance = HycomDataSet(xdataset_url_2014, ydataset_url_2014)
    dataset_instance.print_datasets()
    Plot(dataset_instance).plot_uv_series(-45, -23, 'vvel')
    # 
    # y_dataset_instance = HycomDataSet(ydataset_url_2014)
    # y_dataset_instance.print_dataset()
    
    # Plot(y_dataset_instance).plot_v_series(-45, -23)
    # Plot(x_dataset_instance).plot_gradient_series(-45, -23)
    # y_dataset_instance
    
    # import pdb; pdb.set_trace()
    # lon = x_dataset_instance.xdataset_persist.Longitude[0, :]
    # import pdb; pdb.set_trace()
    # # Normalize lon values
    # lon = lon - lon[0].values
    # # Set first as -180 and not 0
    # lon = lon - 180
    # # Find indexes of lon range
    # x_indexes = np.where(np.logical_and(lon >= -54, lon <= -30))
    # 
    # dados = x_dataset_instance.data_set_persist.u[1, 1, 1450,  x_indexes[0]]
    # dados.plot()
    
    # x_dataset_instance = HycomDataSet(xdataset_url_2008)
    # plot = Plot('teste')
    # plot.plot_area_buoy()