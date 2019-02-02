import xray
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class HycomDataSet:
    # Initializer / Instance Attributes
    def __init__(self, dataset_url):
        self.dataset_url = dataset_url
        self.data_set_persist = self.load_dataset()

    def print_dataset(self):
        print(self.dataset())
  
    def dataset(self):
        self.data_set_persist = self.data_set_persist or self.load_dataset()
        return self.data_set_persist
    
    def load_dataset(self):
        return xray.open_dataset(self.dataset_url, decode_times=False)
        
    def plot_series(self, lon, lat):
        return self.data_set_persist.u.isel(X=200, Y=1000, Depth=0).plot()
        
        
class Plot:
    
    def __init__(self, hycom_object):
        self.hycom_object = hycom_object
        
    def plot_area_buoy(self):
        import yaml
        
        buoy_station_file='dataset/buoys_stations.yml'
        file = open(buoy_station_file).read()
        data_stations = yaml.load(file)
        # dict_variable = {key:value for (key,value) in data_stations.items()}
        # pd_stations = pd.DataFrame.from_dict(data_stations)
        
        array_lon = []
        array_lat = []
        
        for project in data_stations:
            for station in data_stations[project]:
                lon = data_stations[project][station]['lon']
                lat = data_stations[project][station]['lat']
                
                array_lon = array_lon + [lon]
                array_lat = array_lat + [lat]
            
        minlat = np.array(array_lat).min()
        maxlat = np.array(array_lat).max()
        
        minlon = np.array(array_lon).min()
        maxlon = np.array(array_lon).max()
        # import pdb; pdb.set_trace()
        # self.array_lonlat
        
        central_lat = (minlat + maxlat)/2
        central_lon = (minlon + maxlon)/2
        
        from mpl_toolkits.basemap import Basemap
        import matplotlib.pyplot as plt
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
        
    def find_min_lonlat(self, arg):
        import pdb; pdb.set_trace()
        

if __name__ == "__main__":
        
    xdataset_url = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/uvel'
    ydataset_url = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/vvel'

    # x_dataset_instance = HycomDataSet(xdataset_url)
    # x_dataset_instance.print_dataset()
    # 
    # lon = x_dataset_instance.data_set_persist.Longitude[0, :]
    # # Normalize lon values
    # lon = lon - lon[0].values
    # # Set first as -180 and not 0
    # lon = lon - 180
    # # Find indexes of lon range
    # x_indexes = np.where(np.logical_and(lon >= -54, lon <= -30))
    # 
    # dados = x_dataset_instance.data_set_persist.u[1, 1, 1450,  x_indexes[0]]
    # dados.plot()
    
    # x_dataset_instance = HycomDataSet(xdataset_url)
    plot = Plot('teste')
    plot.plot_area_buoy()