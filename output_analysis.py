# -*- coding: utf-8 -*-

import numpy as np
import yaml
import pandas as pd
import xray
#import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

import os
from tool_scripts import *

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class OutputAnalysis:
    def __init__(self, hycom_url, ww3_url, pnboia_url):
        self.hycom_url = hycom_url
        self.hycom = xray.open_dataset(hycom_url)
        self.year = hycom_url.split('/')[-1].split('.')[1]
        
        self.ww3_url = ww3_url
        self.ww3 = xray.open_dataset(ww3_url)
        
        if pnboia_url:
            self.pnboia_url = pnboia_url
            self.pnboia = xray.open_dataset(pnboia_url)
        
    def check_hs_pnboia(self):
        fig = plt.figure(figsize=(15,8))
        lon = self.pnboia_lonlat()[0]
        lat = self.pnboia_lonlat()[1]
        
        fig_dir = 'results/analysis/pnboia_comparison/%s' % (self.pnboia_url.split("/")[-1].split(".")[0])
        os.system('mkdir -p %s' % fig_dir)
        
        fig_name = '%s/%s_hs_comp_lon_lat_%s_%s.png' % (fig_dir, self.year, lon, lat)
        
        self.hycom['time'] = (self.hycom.time - 24*60*60*1000000000)
        self.ww3['time'] = (self.ww3.time - 24*60*60*1000000000)

        hs_mask = self.pnboia.wave_hs.where((self.pnboia.wave_hs < 12) & (self.pnboia.wave_hs > 0))
        hs_mask2 = hs_mask.where(hs_mask < (np.mean(hs_mask) + (3 * np.std(hs_mask))))
        hs_pnboia = hs_mask2.sel(time=slice(start_end_time_ww3(self.hycom['time'])[0], start_end_time_ww3(self.hycom['time'])[1]))
        
        mask_pnboia = np.isnan(hs_pnboia)
        hs_hycom = self.hycom.hs.sel(time=hs_pnboia.time, longitude=lon, latitude=lat, method='nearest')
        # hs_mercator = self.mercator.hs.sel(time=hs_pnboia.time, longitude=lon, latitude=lat, method='nearest')
        # hs_globcurtot = self.globcurtot.hs.sel(time=hs_pnboia.time, longitude=lon, latitude=lat, method='nearest')
        hs_ww3 = self.ww3.hs.sel(time=hs_pnboia.time, longitude=lon, latitude=lat, method='nearest')

        dist = 40
        cor_hycom      = np.corrcoef(hs_hycom[~mask_pnboia][dist::], hs_pnboia[~mask_pnboia][dist::])
        # cor_mercator   = np.corrcoef(hs_mercator[~mask_pnboia][dist::], hs_pnboia[~mask_pnboia][dist::])
        # cor_globcurtot = np.corrcoef(hs_globcurtot[~mask_pnboia][dist::], hs_pnboia[~mask_pnboia][dist::])
        cor_ww3        = np.corrcoef(hs_ww3[~mask_pnboia][dist::], hs_pnboia[~mask_pnboia][dist::])
        
        textstr = '\n'.join((
            r'hycom $r^{2}=%.2f$' % (cor_hycom[0,1], ),
            # r'$mercator r^{2}=%.2f$' % (cor_mercator[0,1], ),
            # r'$globcurtot r^{2}=%.2f$' % (cor_globcurtot[0,1], ),
            r'sem corrente $r^{2}=%.2f$' % (cor_ww3[0,1], )
            ))
        props = dict(boxstyle='round', facecolor='gray', alpha=0.5)

        # import pdb; pdb.set_trace()
        
        plt.plot(self.hycom.time[dist::], self.hycom.hs.sel(longitude=lon, latitude=lat, method='nearest')[dist::], '-k', label='Hs com corr. hycom')
        # plt.plot(self.hycom.time[dist::], self.mercator.hs.sel(longitude=lon, latitude=lat, method='nearest')[dist::], '*b')
        # plt.plot(self.hycom.time[dist::], self.globcurtot.hs.sel(longitude=lon, latitude=lat, method='nearest')[dist::], '.g')
        plt.plot(self.hycom.time[dist::], self.ww3.hs.sel(longitude=lon, latitude=lat, method='nearest')[dist::], '-y', label='Hs sem corrente')
        plt.plot(hs_pnboia.time, hs_pnboia, '.r', label='Hs pnboia')
        plt.xticks(rotation=30)
        plt.grid()
        plt.legend(loc='upper left')
        
        plt.text(self.hycom.time[-90].values, np.max(hs_pnboia)-0.2, textstr)
        plt.title(u'Comparação Hs com e sem corrente')
        plt.xlabel('tempo')
        plt.ylabel('Hs (m)')
        
        plt.savefig(fig_name)


    def check_vel_pnboia(self, lon, lat):
        fig = plt.figure(figsize=(15,8))
        lon = lon
        lat = lat
        
        fig_dir = 'results/analysis/vel_lon_lat_%s_%s' % (lon, lat)
        os.system('mkdir -p %s' % fig_dir)
        
        fig_name = '%s/%s_hs_comp_lon_lat_%s_%s.png' % (fig_dir, self.year, lon, lat)
        
        hs_hycom = self.hycom.hs.sel(time=hs_pnboia.time, longitude=lon, latitude=lat, method='nearest')
        
        import pdb; pdb.set_trace()

        textstr = '\n'.join((
            r'hycom $r^{2}=%.2f$' % (cor_hycom[0,1], ),
            # r'$mercator r^{2}=%.2f$' % (cor_mercator[0,1], ),
            # r'$globcurtot r^{2}=%.2f$' % (cor_globcurtot[0,1], ),
            r'sem corrente $r^{2}=%.2f$' % (cor_ww3[0,1], )
            ))
        props = dict(boxstyle='round', facecolor='gray', alpha=0.5)

        # import pdb; pdb.set_trace()
        dist = 40
        
        plt.plot(self.hycom.time[dist::], self.hycom.hs.sel(longitude=lon, latitude=lat, method='nearest')[dist::], '-k', label='Hs com corr. hycom')
        plt.plot(self.hycom.time[dist::], self.hycom.hs.sel(longitude=lon, latitude=lat, method='nearest')[dist::], '-y', label='Hs sem corrente')
        plt.xticks(rotation=30)
        plt.grid()
        plt.legend(loc='upper left')
        
        plt.text(self.hycom.time[-90].values, np.max(hs_pnboia)-0.2, textstr)
        plt.title(u'Velocidade corrente')
        plt.xlabel('tempo')
        plt.ylabel('velocidade (m/s)')
        
        plt.savefig(fig_name)
        
                
    def pnboia_lonlat(self):
        lon = self.pnboia.longitude.values[-1]
        lat = self.pnboia.latitude.values[-1]
        
        return lon, lat