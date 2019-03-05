# -*- coding: utf-8 -*-

import numpy as np
import yaml
import pandas as pd
import xray
#import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
# plt.switch_backend('agg')
import os
from tool_scripts import *

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class PlotResults:
    def __init__(self, ww3_cur_path, ww3_no_cur_path, pnboia_path=None):
        self.ww3_cur_experiment = ww3_cur_path.split('/')[-1].split('.')[0]
        self.ww3_cur_year = ww3_cur_path.split('/')[-1].split('.')[1]
        self.ww3_cur = xray.open_dataset(ww3_cur_path)
        
        self.ww3_no_cur = xray.open_dataset(ww3_no_cur_path)
        
        if pnboia_path:
            self.pnboia_path = pnboia_path
            self.pnboia = xray.open_dataset(pnboia_path)
        
    def year(self):
        ntime = self.ww3_cur.time.size / 2
        seltime = self.ww3_cur.time[ntime].time.values
        year = pd.to_datetime(str(seltime)).strftime('%Y')

        return year
    
    def start_end_time_ww3(self, dtime):
        start = pd.to_datetime(str(dtime[0].values)).strftime('%Y-%m-%d')
        end = pd.to_datetime(str(dtime[-1].values)).strftime('%Y-%m-%d')
        return [start, end]
        
    def plot_video_curr_no_curr(self):
        pass
        
    def hs_comparison(self, lon, lat):
        fig_dir = 'results/analysis'
        fig_path = '%s/%s_%s_%s_%s' % (fig_dir, self.year(), lon, lat, 'comp_hs_cur_no.png')
        
        hs_cur = self.ww3_cur.hs.sel(longitude=lon, latitude=lat, method='nearest')
        hs_no_cur = self.ww3_no_cur.hs.sel(longitude=lon, latitude=lat, method='nearest')
        
        # import pdb; pdb.set_trace()
        plt.figure(figsize=(12,6))
        
        plt.plot(hs_cur.time, hs_cur, '.k', label='Hs com corrente')
        plt.plot(hs_cur.time, hs_no_cur, '-g', label='Hs sem corrente')
        plt.legend()
        plt.xticks(rotation=30)
        plt.grid()
        
        # plt.savefig(fig_path)
        # plt.close()
        
    def hs_comparison_pnboia(self):
        fig_dir = 'results/analysis'
        lon = self.pnboia.variables['longitude'][-1].values
        lat = self.pnboia.variables['latitude'][-1].values
        
        fig_path = '%s/pnboia_%s_%s_%s_%s' % (fig_dir, self.year(), lon, lat, 'comp_hs_cur_no.png')
        
        hs_cur = self.ww3_cur.hs.sel(longitude=lon, latitude=lat, method='nearest')
        hs_no_cur = self.ww3_no_cur.hs.sel(longitude=lon, latitude=lat, method='nearest')
        
        hs_cur['time'] = (hs_cur.time - 24*60*60*1000000000)
        hs_no_cur['time'] = (hs_no_cur.time - 24*60*60*1000000000)

        hs_mask = self.pnboia.wave_hs.where((self.pnboia.wave_hs < 12) & (self.pnboia.wave_hs > 0))
        hs_mask2 = hs_mask.where(hs_mask < (np.mean(hs_mask) + (3 * np.std(hs_mask))))
        hs_pnboia = hs_mask2.sel(time=slice(self.start_end_time_ww3(hs_no_cur['time'])[0], self.start_end_time_ww3(hs_no_cur['time'])[1]))
        
        mask_pnboia = np.isnan(hs_pnboia)
        hs_no_cur_pnboia = hs_no_cur.sel(time=hs_pnboia.time, method='nearest')
        hs_cur_pnboia = hs_cur.sel(time=hs_pnboia.time, method='nearest')
        
        discard_time = 50        
        
        cur_correlation = np.corrcoef(hs_cur_pnboia[~mask_pnboia][discard_time::], hs_pnboia[~mask_pnboia][discard_time::])
        no_cur_correlation = np.corrcoef(hs_no_cur_pnboia[~mask_pnboia][discard_time::], hs_pnboia[~mask_pnboia][discard_time::])
        
        # import pdb; pdb.set_trace()
        
        plt.figure(figsize=(12,6))
        
        plt.plot(hs_cur.time[discard_time::], hs_cur[discard_time::], '-k', label='Hs com corrente')
        plt.plot(hs_no_cur.time[discard_time::], hs_no_cur[discard_time::], '-g', label='Hs sem corrente')
        plt.plot(hs_pnboia.time, hs_pnboia, '.r', label='Hs bóia')
        plt.legend()
        title = u'correlação (r) sem corrente = %s \ncorrelação (r) com corrente = %s ' % (no_cur_correlation[0,1], cur_correlation[0,1])
        plt.title('%s' % (title))
        # import pdb; pdb.set_trace()
        
        plt.text(pd.to_datetime(str(hs_pnboia.time[-10].values)), 3 ,'teste')
        
        plt.xticks(rotation=30)
        plt.grid()
        
        plt.savefig(fig_path)
        plt.close()
    
    def make_video(self):
        from mpl_toolkits.basemap import Basemap
        # import pdb; pdb.set_trace();
        fig_dir1 = 'results/analysis/videos'
        fig_dir = '%s/%s/%s' % (fig_dir1, self.ww3_cur_experiment, self.ww3_cur_year)
        
        os.system('mkdir -p %s' % (fig_dir))
        # import pdb; pdb.set_trace()
        time_dist = 6
        lon = self.ww3_cur.longitude.values
        lat = self.ww3_cur.latitude.values
        
        for time in self.ww3_no_cur.time[::time_dist]:
            fig_name = '%s/%s_hs_cur_%s_.jpg' % (fig_dir, self.ww3_cur_experiment, pd.to_datetime(str(time.values)).strftime("%Y%m%d%H"))
            print('Plotting %s' % (fig_name))
            
            fig = plt.figure(figsize=(13,13))
            # import pdb; pdb.set_trace()
            ax1 = plt.subplot2grid((4, 4), (0,0), rowspan=2, colspan=2)
            ax2 = plt.subplot2grid((4, 4), (0,2), rowspan=2, colspan=2)
            ax3 = plt.subplot2grid((4, 4), (2,1), rowspan=2, colspan=2)
            
            max_hs = 4
            min_hs = 0
            
            # import pdb; pdb.set_trace()
            m1 = Basemap(projection='merc',llcrnrlat=np.min(lat) - 1,urcrnrlat=np.max(lat) + 1, llcrnrlon=np.min(lon) - 1,urcrnrlon=np.max(lon) + 1,lat_ts=-20,resolution='l', ax=ax1)
            lons2d, lats2d = np.meshgrid(lon, lat)
            x, y = m1(lons2d, lats2d)
            m1.drawmapboundary()
            m1.drawcoastlines()
            
            m1.drawparallels(np.arange(np.round(m1.llcrnrlat),np.round(m1.urcrnrlat), 2.), labels=[1,0,0,0], color='k', dashes=[1, 4])
            m1.drawmeridians(np.arange(np.round(m1.llcrnrlon),np.round(m1.urcrnrlon), 2.), labels=[0,0,0,1], color='k', dashes=[1, 4])
            
            ax1.set_title('Hs with current')
            c1 = m1.pcolormesh(x, y, self.ww3_cur.hs.sel(time=time, method='nearest'), cmap='jet', vmin=min_hs, vmax=max_hs)
            # fig.colorbar(c1, ax=ax2, label='Hs (m)')
            
            m2 = Basemap(projection='merc',llcrnrlat=np.min(lat) - 1,urcrnrlat=np.max(lat) + 1, llcrnrlon=np.min(lon) - 1,urcrnrlon=np.max(lon) + 1,lat_ts=-20,resolution='l', ax=ax2)
            # x, y = m1(lons2d, lats2d)
            m2.drawmapboundary()
            m2.drawcoastlines()
            
            m2.drawparallels(np.arange(np.round(m1.llcrnrlat),np.round(m1.urcrnrlat), 2.), labels=[1,0,0,0], color='k', dashes=[1, 4])
            m2.drawmeridians(np.arange(np.round(m1.llcrnrlon),np.round(m1.urcrnrlon), 2.), labels=[0,0,0,1], color='k', dashes=[1, 4])
            
            ax2.set_title('Hs without current')
            c2 = m2.pcolormesh(x, y, self.ww3_no_cur.hs.sel(time=time, method='nearest'), cmap='jet', vmin=min_hs, vmax=max_hs)
            fig.colorbar(c2, ax=[ax1, ax2], label='Hs (m)')
            
            m3 = Basemap(projection='merc',llcrnrlat=np.min(lat) - 1,urcrnrlat=np.max(lat) + 1, llcrnrlon=np.min(lon) - 1,urcrnrlon=np.max(lon) + 1,lat_ts=-20,resolution='l', ax=ax3)
            m3.drawmapboundary()
            m3.drawcoastlines()
            
            m3.drawparallels(np.arange(np.round(m1.llcrnrlat),np.round(m1.urcrnrlat), 2.), labels=[1,0,0,0], color='k', dashes=[1, 4])
            m3.drawmeridians(np.arange(np.round(m1.llcrnrlon),np.round(m1.urcrnrlon), 2.), labels=[0,0,0,1], color='k', dashes=[1, 4])
            
            # import pdb; pdb.set_trace()
            vel = np.sqrt(self.ww3_cur.ucur.sel(time=time, method='nearest') ** 2 + self.ww3_cur.vcur.sel(time=time, method='nearest') ** 2)
            
            ax3.set_title('Current from %s' % (self.ww3_cur_experiment.split("_")[-1]) )
            c3 = m3.pcolormesh(x, y, vel, cmap='jet', vmin=0, vmax=1.5)
            fig.colorbar(c3, ax=ax3, label='Velocity (m/s)')
            
            fig.suptitle('\n%s run with and without current for year %s \n\n dt = %sH' % (self.ww3_cur_experiment, self.ww3_cur_year, pd.to_datetime(str(time.values)).strftime("%Y%m%d %H") ), fontsize=18)
            
            # dist = 6
            # [u, v] = self.hycom_object.u_v_2d(i1, i2, j1, j2, iindex)
            # m.quiver(x[::dist, ::dist], y[::dist, ::dist], u[::dist, ::dist], v[::dist, ::dist], color='k')
            
            plt.savefig(fig_name)
            plt.close("all")
            
        cmd = "ffmpeg -y -r 8 -pattern_type glob -i '%s/*.jpg' -c:v libx264 %s_%s.mp4" % (fig_dir, self.ww3_cur_experiment, self.ww3_cur_year)
        os.system(cmd)
        
    def make_video_regional(self):
        from mpl_toolkits.basemap import Basemap
        pnboia_cabofrio = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Bcabo_frio2.nc')
        pnboia_santos = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Bsantos.nc')
        pnboia_flo = xray.open_dataset('http://goosbrasil.org:8080/pnboia/Bsanta_catarina.nc')
        
        lon_stations = [pnboia_cabofrio.longitude[-1].values]
        lon_stations.append(pnboia_santos.longitude[-1].values)
        lon_stations.append(pnboia_flo.longitude[-1].values)
        
        lat_stations = [pnboia_cabofrio.latitude[-1].values]
        lat_stations.append(pnboia_santos.latitude[-1].values)
        lat_stations.append(pnboia_flo.latitude[-1].values)
        
        # [u, v] = getuv(self.ww3_cur.hs[100], self.ww3_cur.dir[100])
        # import pdb; pdb.set_trace();

        data_stations = get_yaml('dataset/buoys_stations.yml')
        [array_lon, array_lat] = array_stations(data_stations)

        minlat = np.array(array_lat).min() - 1.5
        maxlat = np.array(array_lat).max() + 1.5
        minlon = np.array(array_lon).min() - 1.5
        maxlon = np.array(array_lon).max() + 1.5

        # import pdb; pdb.set_trace();
        
        fig_dir1 = 'results/analysis/videos'
        fig_dir = '%s/%s/%s_regional' % (fig_dir1, self.ww3_cur_experiment, self.ww3_cur_year)
        
        os.system('mkdir -p %s' % (fig_dir))
        # import pdb; pdb.set_trace()
        time_dist = 6
        lon = self.ww3_cur.longitude
        lat = self.ww3_cur.latitude
        
        for time in self.ww3_no_cur.time[::time_dist]:
            fig_name = '%s/%s_hs_cur_%s_.jpg' % (fig_dir, self.ww3_cur_experiment, pd.to_datetime(str(time.values)).strftime("%Y%m%d%H"))
            print('Plotting %s' % (fig_name))
        
            fig = plt.figure(figsize=(10,10))
            # import pdb; pdb.set_trace()
            ax1 = plt.subplot2grid((4, 4), (0,0), rowspan=2, colspan=2)
            ax2 = plt.subplot2grid((4, 4), (0,2), rowspan=2, colspan=2)
            ax3 = plt.subplot2grid((4, 4), (2,2), rowspan=2, colspan=2)
            ax4 = plt.subplot2grid((4, 4), (2,0), rowspan=2, colspan=2)
        
            max_hs = 3
            min_hs = 0
        
            m1 = Basemap(projection='merc',llcrnrlat=minlat,urcrnrlat=maxlat, llcrnrlon=minlon,urcrnrlon=maxlon,lat_ts=-20,resolution='l', ax=ax1)
            # import pdb; pdb.set_trace()
            lons2d, lats2d = np.meshgrid(lon.sel(longitude=slice(minlon, maxlon)), lat.sel(latitude=slice(minlat, maxlat)))
        
            x, y = m1(lons2d, lats2d)
            m1.drawmapboundary()
            m1.drawcoastlines()
            m1.fillcontinents(color='gray')
        
            m1.drawparallels(np.arange(np.round(m1.llcrnrlat),np.round(m1.urcrnrlat), 2.), labels=[1,0,0,0], color='k', dashes=[1, 4])
            m1.drawmeridians(np.arange(np.round(m1.llcrnrlon),np.round(m1.urcrnrlon), 2.), labels=[0,0,0,1], color='k', dashes=[1, 4])
            
            x_stations, y_stations = m1(lon_stations, lat_stations)
            m1.scatter(x_stations, y_stations, 30, marker='o', color='black', zorder=2)
            
            ax1.set_title('Hs com corrente')
            hs_cur = self.ww3_cur.hs.sel(time=time, longitude=slice(minlon, maxlon), latitude=slice(minlat, maxlat))
            c1 = m1.pcolormesh(x, y, self.ww3_cur.hs.sel(time=time, longitude=slice(minlon, maxlon), latitude=slice(minlat, maxlat)), cmap='jet', vmin=min_hs, vmax=max_hs)
            dist = 6
            m1.quiver(x[::dist, ::dist], y[::dist, ::dist], -np.sin(hs_cur)[::dist, ::dist], -np.cos(hs_cur)[::dist, ::dist], width=0.005, scale=20)
            # fig.colorbar(c1, ax=ax2, label='Hs (m)')
        
            m2 = Basemap(projection='merc',llcrnrlat=minlat,urcrnrlat=maxlat, llcrnrlon=minlon,urcrnrlon=maxlon,lat_ts=-20,resolution='l', ax=ax2)
            # x, y = m1(lons2d, lats2d)
            m2.drawmapboundary()
            m2.drawcoastlines()
            m2.fillcontinents(color='gray')
        
            m2.drawparallels(np.arange(np.round(m1.llcrnrlat),np.round(m1.urcrnrlat), 2.), labels=[0,0,0,0], color='k', dashes=[1, 4])
            m2.drawmeridians(np.arange(np.round(m1.llcrnrlon),np.round(m1.urcrnrlon), 2.), labels=[0,0,0,1], color='k', dashes=[1, 4])
            m2.scatter(x_stations, y_stations, 30, marker='o', color='black', zorder=2)
        
            ax2.set_title('Hs sem corrente')
            hs_no_cur = self.ww3_no_cur.hs.sel(time=time, longitude=slice(minlon, maxlon), latitude=slice(minlat, maxlat))
            c2 = m2.pcolormesh(x, y, hs_no_cur, cmap='jet', vmin=min_hs, vmax=max_hs)
            
            dist = 6
            m2.quiver(x[::dist, ::dist], y[::dist, ::dist], -np.sin(hs_no_cur)[::dist, ::dist], -np.cos(hs_no_cur)[::dist, ::dist], width=0.005, scale=20)
            fig.colorbar(c2, ax=[ax1, ax2], label='Hs (m)')
        
            m3 = Basemap(projection='merc',llcrnrlat=minlat,urcrnrlat=maxlat, llcrnrlon=minlon,urcrnrlon=maxlon,lat_ts=-20,resolution='l', ax=ax3)
            m3.drawmapboundary()
            m3.drawcoastlines()
            m3.fillcontinents(color='gray')
            m3.scatter(x_stations, y_stations, 30, marker='o', color='black', zorder=2)
        
            m3.drawparallels(np.arange(np.round(m1.llcrnrlat),np.round(m1.urcrnrlat), 2.), labels=[0,0,0,0], color='k', dashes=[1, 4])
            m3.drawmeridians(np.arange(np.round(m1.llcrnrlon),np.round(m1.urcrnrlon), 2.), labels=[0,0,0,1], color='k', dashes=[1, 4])
        
            # import pdb; pdb.set_trace()
            u_cur = self.ww3_cur.ucur.sel(time=time, longitude=slice(minlon, maxlon), latitude=slice(minlat, maxlat))
            v_cur = self.ww3_cur.vcur.sel(time=time, longitude=slice(minlon, maxlon), latitude=slice(minlat, maxlat))
            
            vel = np.sqrt(u_cur ** 2 + v_cur ** 2)
        
            ax3.set_title('Corrente %s' % (self.ww3_cur_experiment.split("_")[-1]) )
            c3 = m3.pcolormesh(x, y, vel, cmap='jet', vmin=0, vmax=1.5)
            dist = 6
            
            m3.quiver(x[::dist, ::dist], y[::dist, ::dist], u_cur[::dist, ::dist], v_cur[::dist, ::dist], width=0.005, scale=18)
            fig.colorbar(c3, ax=ax3, label='Velocidade (m/s)')
            
            m4 = Basemap(projection='merc',llcrnrlat=minlat,urcrnrlat=maxlat, llcrnrlon=minlon,urcrnrlon=maxlon,lat_ts=-20,resolution='l', ax=ax4)
            # x, y = m1(lons2d, lats2d)
            m4.drawmapboundary()
            m4.drawcoastlines()
            m4.fillcontinents(color='gray')
        
            m4.drawparallels(np.arange(np.round(m1.llcrnrlat),np.round(m1.urcrnrlat), 2.), labels=[1,0,0,0], color='k', dashes=[1, 4])
            m4.drawmeridians(np.arange(np.round(m1.llcrnrlon),np.round(m1.urcrnrlon), 2.), labels=[0,0,0,1], color='k', dashes=[1, 4])
            m4.scatter(x_stations, y_stations, 30, marker='o', color='black', zorder=2)
        
            ax4.set_title(u'Diferença entre Hs_curr - Hs_no_curr')
            hs_diff = hs_cur - hs_no_cur
            c4 = m4.pcolormesh(x, y, hs_diff, cmap='jet', vmin=-0.4, vmax=0.4)
            fig.colorbar(c4, ax=ax4, label='Hs dif (m)')
        
            fig.suptitle('\n%s experimento com e sem corrente para o ano %s \n\n dt = %sH' % (self.ww3_cur_experiment, self.ww3_cur_year, pd.to_datetime(str(time.values)).strftime("%Y%m%d %H") ), fontsize=18)
        
            plt.savefig(fig_name)
            plt.close("all")
            
        cmd = "ffmpeg -y -r 8 -pattern_type glob -i '%s/*.jpg' -c:v libx264 %s_%s_regional_lat_lon_%s_%s.mp4" % (fig_dir, self.ww3_cur_experiment, self.ww3_cur_year, minlat, minlon)
        os.system(cmd)
        
    def tp_comparison(self, lon, lat):
        fig_dir = 'results/analysis'
        fig_path = '%s/%s_%s_%s_%s' % (fig_dir, self.year(), lon, lat, 'comp_tp_cur_no.png')
        
        tp_cur = self.ww3_cur.t0.sel(longitude=lon, latitude=lat, method='nearest')
        tp_no_cur = self.ww3_no_cur.t0.sel(longitude=lon, latitude=lat, method='nearest')
        
        plt.plot(tp_cur[10::].time, tp_cur[10::], '.k')
        plt.plot(tp_cur[10::].time, tp_no_cur[10::], '-g')
        plt.xticks(rotation=30)
        
        plt.savefig(fig_path)
        plt.close()