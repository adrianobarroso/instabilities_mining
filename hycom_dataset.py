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

    def load_dataset(self):
        self.xdataset_persist = xray.open_dataset(self.xdataset_url, decode_times=False)
        self.ydataset_persist = xray.open_dataset(self.ydataset_url, decode_times=False)
        self.set_lon_lat_array_coordinates()
        self.set_time_series_coordinate()

    def vel_series_lon_lat(self, lon, lat):
        ix = find_nearest_value_index(self.lon_array, lon)
        iy = find_nearest_value_index(self.lat_array, lat)

        useries = self.xdataset_persist.u.isel(X=ix[1], Y=iy[1], Depth=0)
        vseries = self.ydataset_persist.v.isel(X=ix[1], Y=iy[1], Depth=0)

        return np.sqrt((useries ** 2) + (vseries ** 2))

    def vel(self, i1, i2, j1, j2):
        uvel = self.xdataset_persist.u.isel(X=slice(i1,i2), Y=slice(j1,j2), Depth=0, MT=140)
        vvel = self.ydataset_persist.v.isel(X=slice(i1,i2), Y=slice(j1,j2), Depth=0, MT=140)

        return np.sqrt((vvel * vvel) + (uvel * uvel))

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
        plt.close()

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

        dir = 'images/lon_%s_lat_%s/' % (lon, lat)

        os.system('mkdir -p %s' % (dir))

        fig.savefig('images/lon_%s_lat_%s/%s' %  (lon, lat, fig_name))
        plt.close()

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

        os.system('mkdir -p %s' % (dir))

        fig.savefig('images/lon_%s_lat_%s/%s' %  (lon, lat, fig_name))

    def quiver_plot(self):
        from mpl_toolkits.basemap import Basemap

        data_stations = self.get_yaml('dataset/buoys_stations.yml')
        [array_lon, array_lat] = array_stations(data_stations)

        minlat = np.array(array_lat).min()
        maxlat = np.array(array_lat).max()
        minlon = np.array(array_lon).min()
        maxlon = np.array(array_lon).max()

        central_lat = (minlat + maxlat)/2
        central_lon = (minlon + maxlon)/2

        # setup Lambert Conformal basemap.
        m = Basemap(width=3500000,height=2000000,projection='lcc', resolution='l',lat_1=minlat,lat_2=maxlat,lat_0=central_lat,lon_0=central_lon)


        [_l, i1] = find_nearest_value_index(self.hycom_object.lon_array, np.round(m.llcrnrlon))
        [_l, i2] = find_nearest_value_index(self.hycom_object.lon_array, np.round(m.urcrnrlon))

        [_l, j1] = find_nearest_value_index(self.hycom_object.lat_array, np.round(m.llcrnrlat))
        [_l, j2] = find_nearest_value_index(self.hycom_object.lat_array, np.round(m.urcrnrlat))

        vel = self.hycom_object.vel(i1, i2, j1, j2)

        # import pdb; pdb.set_trace()

        m.drawcoastlines()
        # m.bluemarble()
        x, y = m(array_lon, array_lat)
        m.scatter(x, y, 30, marker='o', color='red', zorder=100)


        m.drawparallels(np.arange(np.round(m.llcrnrlat),np.round(m.urcrnrlat),5.), labels=[0,1,0,0], color='white', dashes=[1, 4])
        m.drawmeridians(np.arange(np.round(m.llcrnrlon),np.round(m.urcrnrlon),10.), labels=[0,0,0,1], color='white', dashes=[1, 4])

        m.drawmapboundary()

        # c = m.contourf(self.hycom_object.xdataset_persist.Longitude.isel(X=slice(i1,i2), Y=slice(j1,j2)).values - 78 -180, self.hycom_object.xdataset_persist.Latitude.isel(X=slice(i1,i2), Y=slice(j1,j2)).values, vel.values, cmap='jet')
        import pdb; pdb.set_trace()
        m.contourf((self.hycom_object.lon_array[i1:i2]-78-180), self.hycom_object.lat_array[j1:j2], vel.values, cmap='jet')
        # c = plt.contourf(self.hycom_object.lon_array.isel(X=slice(i1,i2), Y=slice(j1,j2)), self.hycom_object.lat_array.isel(X=slice(i1,i2), Y=slice(j1,j2)), vel, cmap='jet')
