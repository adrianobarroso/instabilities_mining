import numpy as np
import yaml
#import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
plt.switch_backend('agg')
import os

from tool_scripts import *

class Plot:
    def __init__(self, hycom_object):
        self.hycom_object = hycom_object

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

    def quiver_plot(self, dt, range_vel):
        from mpl_toolkits.basemap import Basemap

        data_stations = get_yaml('dataset/buoys_stations.yml')
        [array_lon, array_lat] = array_stations(data_stations)

        minlat = np.array(array_lat).min() - 3
        maxlat = np.array(array_lat).max() + 3
        minlon = np.array(array_lon).min() - 3
        maxlon = np.array(array_lon).max() + 3

        import pdb; pdb.set_trace();

        [_l, i1] = find_nearest_value_index(self.hycom_object.lon_array, np.round(minlon))
        [_l, i2] = find_nearest_value_index(self.hycom_object.lon_array, np.round(maxlon))
        
        [_l, j1] = find_nearest_value_index(self.hycom_object.lat_array, np.round(minlat))
        [_l, j2] = find_nearest_value_index(self.hycom_object.lat_array, np.round(maxlat))
        
        lon = self.hycom_object.xdataset_persist.Longitude.isel(X=slice(i1,i2), Y=slice(j1,j2)).values - 360
        lat = self.hycom_object.xdataset_persist.Latitude.isel(X=slice(i1,i2), Y=slice(j1,j2)).values
        
        m = Basemap(projection='merc',llcrnrlat=np.min(lat),urcrnrlat=np.max(lat), llcrnrlon=np.min(lon),urcrnrlon=np.max(lon),lat_ts=-20,resolution='l')
        # 
        x, y = m(lon, lat)
        
        vel = self.hycom_object.vel(i1, i2, j1, j2, dt)
        fig_name = 'images/mapas/vel/mapa_ano_%s_index_%s_.jpg' % (str(vel.Date.values), str(vel.MT.values))
        
        [u, v] = self.hycom_object.u_v_2d(i1, i2, j1, j2, dt)

        # import pdb; pdb.set_trace()

        m.drawmapboundary()
        m.drawcoastlines()
        # m.bluemarble()
        x_stations, y_stations = m(array_lon, array_lat)
        m.scatter(x_stations, y_stations, 30, marker='o', color='black', zorder=100)

        m.drawparallels(np.arange(np.round(m.llcrnrlat),np.round(m.urcrnrlat),4.), labels=[1,0,0,0], color='white', dashes=[1, 4])
        m.drawmeridians(np.arange(np.round(m.llcrnrlon),np.round(m.urcrnrlon),4.), labels=[0,0,0,1], color='white', dashes=[1, 4])

        c = m.pcolormesh(x, y, vel.values, cmap='jet', vmin=range_vel[0], vmax=range_vel[1])
        plt.title('Snapshot hycom current for %s \n MT = %s' % (str(vel.Date.values), str(vel.MT.values)) )

        plt.colorbar(ticks=np.linspace(range_vel[0], range_vel[1], 13), label='velocity (m/s)')
        plt.clim(range_vel[0], range_vel[1])
        
        # import pdb; pdb.set_trace()
        # m.quiver(x, y, u, v)
        dist = 6
        m.quiver(x[::dist, ::dist], y[::dist, ::dist], u[::dist, ::dist], v[::dist, ::dist], color='k')
        # m.quiver(x[::dist, ::dist], y[::dist, ::dist], u[::dist, ::dist], v[::dist, ::dist], vel[::dist, ::dist])
        
        os.system('mkdir -p %s' % ('images/mapas/vel/'))
        
        plt.savefig(fig_name)
        plt.close()
        # m.contourf((self.hycom_object.lon_array[i1:i2]-78-180), self.hycom_object.lat_array[j1:j2], vel.values, cmap='jet')
