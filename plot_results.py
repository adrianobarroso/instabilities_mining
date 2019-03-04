import numpy as np
import yaml
import pandas as pd
#import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
# plt.switch_backend('agg')
import os
from tool_scripts import *

class PlotResults:
    def __init__(self, ww3_cur, ww3_no_cur, pnboia=None):
        self.ww3_cur = ww3_cur
        self.ww3_no_cur = ww3_no_cur
        self.pnboia = pnboia
        
    def year(self):
        ntime = self.ww3_cur.time.size / 2
        seltime = self.ww3_cur.time[ntime].time.values
        year = pd.to_datetime(str(seltime)).strftime('%Y')

        return year
    
    def start_end_time_ww3(self):
        start = pd.to_datetime(str(self.ww3_cur.time[0].values)).strftime('%Y-%m-%d')
        end = pd.to_datetime(str(self.ww3_cur.time[-1].values)).strftime('%Y-%m-%d')
        return [start, end]
        
    def plot_video_curr_no_curr(self):
        pass
        
    def hs_comparison(self, lon, lat):
        fig_dir = 'results/analysis'
        fig_path = '%s/%s_%s_%s_%s' % (fig_dir, self.year(), lon, lat, 'comp_hs_cur_no.png')
        
        hs_cur = self.ww3_cur.hs.sel(longitude=lon, latitude=lat, method='nearest')
        hs_no_cur = self.ww3_no_cur.hs.sel(longitude=lon, latitude=lat, method='nearest')
        
        # import pdb; pdb.set_trace()
        plt.figure(figsize=(20,10))
        
        plt.plot(hs_cur.time, hs_cur, '.k')
        plt.plot(hs_cur.time, hs_no_cur, '-g')
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

        hs_mask = self.pnboia.wave_hs.where((self.pnboia.wave_hs < 12) & (self.pnboia.wave_hs > 0))
        hs_mask2 = hs_mask.where(hs_mask < (np.mean(hs_mask) + (3*np.std(hs_mask))))
        # import pdb; pdb.set_trace()
        hs = hs_mask2.sel(time=slice(self.start_end_time_ww3()[0], self.start_end_time_ww3()[1]))
        
        plt.figure(figsize=(20,10))
        
        discard_time = 50
        
        plt.plot((hs_cur.time - 21*60*60*1000000000)[discard_time::], hs_cur[discard_time::], '-k', label='Hs with current')
        plt.plot((hs_no_cur.time - 21*60*60*1000000000)[discard_time::], hs_no_cur[discard_time::], '-g', label='Hs without current')
        plt.plot(hs.time, hs, '.r', label='Hs from buoy')
        plt.legend()
        plt.xticks(rotation=30)
        plt.grid()
        
        plt.savefig(fig_path)
        plt.close()
        
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