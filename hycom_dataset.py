import xray
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import yaml
import os
from plot_scripts import *

class HycomDataSet:
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
        
    def get_yaml(self, arg):
        yaml_file=arg
        file = open(yaml_file).read()
        return yaml.load(file)
    
    def plot_area_buoy(self):
        from mpl_toolkits.basemap import Basemap
        
        data_stations = get_yaml('dataset/buoys_stations.yml')
        [array_lon, array_lat] = array_stations(data_stations)

        minlat = np.array(array_lat).min()
        maxlat = np.array(array_lat).max()
        minlon = np.array(array_lon).min()
        maxlon = np.array(array_lon).max()
        
        central_lat = (minlat + maxlat)/2
        central_lon = (minlon + maxlon)/2    
        
        # setup Lambert Conformal basemap.
        m = Basemap(width=3500000,height=2000000,projection='lcc',
                    resolution='l',lat_1=minlat,lat_2=maxlat,lat_0=central_lat,lon_0=central_lon)
        m.drawcoastlines()
        m.bluemarble()
        x, y = m(array_lon, array_lat)
        m.scatter(x, y, 30, marker='o', color='red', zorder=100)
        
        # import pdb; pdb.set_trace()

        m.drawparallels(np.arange(np.round(m.llcrnrlat),np.round(m.urcrnrlat),5.), labels=[0,1,0,0], color='white', dashes=[1, 4])
        m.drawmeridians(np.arange(np.round(m.llcrnrlon),np.round(m.urcrnrlon),10.), labels=[0,0,0,1], color='white', dashes=[1, 4])
        
        # for project in data_stations:
        #     for station in data_stations[project]:
        #         lon = data_stations[project][station]['lon']
        #         lat = data_stations[project][station]['lat']
        #         plt.annotate('Barcelona', xy=(m.urcrnrlon, m.llcrnrlat),  xycoords='data',
        #                         xytext=(lon, lat), textcoords='offset points',
        #                         color='r',
        #                         arrowprops=dict(arrowstyle="fancy", color='g')
        #                         )
                                
        # draw a boundary around the map, fill the background.
        # this background will end up being the ocean color, since
        # the continents will be drawn on top.
        # fill continents, set lake color same as ocean color.
        # m.fillcontinents(color='black',lake_color='aqua')
        m.drawmapboundary()
        
        plt.savefig('images/area_buoys.jpg')
        
    def plot_uv_series(self, lon, lat):        
        ix = find_nearest_value_index(self.hycom_object.lon_array, lon)
        iy = find_nearest_value_index(self.hycom_object.lat_array, lat)
        # import pdb; pdb.set_trace()
        [run, exp, year] = self.hycom_object.xdataset_url.split('/')[-4:-1]
        
        fig_name = '%s_HYCOM_%s_%s.jpg' % (year, run, exp)
        
        useries = self.hycom_object.ydataset_persist.v.isel(X=ix[1], Y=iy[1], Depth=0)
        vseries = self.hycom_object.xdataset_persist.u.isel(X=ix[1], Y=iy[1], Depth=0)
            
        # import pdb; pdb.set_trace()
        fig = plt.figure()
        # ax2 = plt.axes([0.55, 0.05, 1, 0.2])
        plt.subplot(2, 1, 1)
        useries.plot()
        plt.xlabel('')
        plt.ylabel('u (m/s)')
        
        plt.subplot(2, 1, 2)
        vseries.plot()
        plt.title('')
        plt.xlabel('time in year ' + year)
        plt.ylabel('v (m/s)')
        
        fig.savefig('images/' + fig_name)
        
    def plot_gradient_series(self, lon, lat):
        ix = find_nearest_value_index(self.hycom_object.lon_array, lon)
        iy = find_nearest_value_index(self.hycom_object.lat_array, lat)
        # import pdb; pdb.set_trace()
        [run, exp, year] = self.hycom_object.xdataset_url.split('/')[-4:-1]
        
        fig_name = 'gradients_%s_HYCOM_%s_%s.jpg' % (year, run, exp)
        
        useries = self.hycom_object.ydataset_persist.v.isel(X=ix[1], Y=iy[1], Depth=0)
        vseries = self.hycom_object.xdataset_persist.u.isel(X=ix[1], Y=iy[1], Depth=0)
            
        # import pdb; pdb.set_trace()
        fig = plt.figure()
        # ax2 = plt.axes([0.55, 0.05, 1, 0.2])
        plt.subplot(2, 1, 1)
        plt.plot(useries.MT.values, np.gradient(useries))
        plt.xlabel('')
        plt.ylabel('gradient u')
        
        plt.subplot(2, 1, 2)
        plt.plot(useries.MT.values, np.gradient(vseries))
        plt.title('')
        plt.xlabel('time in year ' + year)
        plt.ylabel('gradient v')
        dir = 'images/lon_%s_lat_%s/' % (lon, lat)
        
        os.system('mkdir %s' % (dir))
        
        fig.savefig('images/lon_%s_lat_%s/%s' %  (lon, lat, fig_name))