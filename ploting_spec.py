import xray
import numpy as np
import pandas as pd
import os
import sys
from matplotlib import pyplot as plt

ef = xray.open_dataset('results/netcdf_files/ww3_hycom.2016_ef.nc') 
ef_nocur = xray.open_dataset('results/netcdf_files/ww3_nocur.2016_ef.nc') 

lon = float(sys.argv[1])
lat = float(sys.argv[2])
# import pdb; pdb.set_trace()
year = pd.to_datetime(ef.time[100].values).strftime('%Y')

dir_analysis = 'results/analysis/ef/lon_lat_%s_%s/' % (lon, lat)
if sys.argv[3] == 'log':
    dir_video = 'results/analysis/ef/lon_lat_%s_%s/video_images_year_%s_log' % (lon, lat, year)
else:
    dir_video = 'results/analysis/ef/lon_lat_%s_%s/video_images_year_%s' % (lon, lat, year)
    
os.system('mkdir -p %s' % dir_video)
# import pdb; pdb.set_trace()

selef = 10**(ef.ef.sel(longitude=lon, latitude=lat, method='nearest'))
selef_nocur = 10**(ef_nocur.ef.sel(longitude=lon, latitude=lat, method='nearest'))

dist = 50

for dt in range(dist, selef_nocur.time.shape[0]):
    print 'Ploting ef for dt %s \n Lon %s | Lat %s' % (dt, lon, lat)

    date = pd.to_datetime(selef.time[dt].values).strftime('%Y-%m-%d %H:%M')

    plt.title('Longitude=%s ; Latitude=%s \nEspectro de energia por frequencia para o tempo %s' % (lon, lat, date))
    plt.plot(selef.f, selef[dt], '-k', label='ef com corrente')
    plt.plot(selef_nocur.f, selef_nocur[dt], '-.g', label='ef sem corrente')
    if sys.argv[3] == 'log':
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim(0.03, 1.0)
        plt.ylim(0.00002, 30.0)
        figname = '%s/log_%03d_spec.png' % (dir_video, dt)
    else:
        plt.ylim(0, 16)
        plt.xlim(0.02, 0.8)
        figname = '%s/%03d_spec.png' % (dir_video, dt)
    plt.xlabel(r'$f$ (Hz)')
    plt.ylabel(r'$E(f) (m^2 / Hz)$')
    plt.legend()
    plt.grid()
    plt.savefig(figname)
    plt.close()

os.system('mkdir -p results/analysis/ef/videos')
if sys.argv[3] == 'log':
    make_video = "ffmpeg -y -r 18 -pattern_type glob -i '%s/*.png' -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p results/analysis/ef/videos/log_ef_%s_lon_lat_%s_%s.mp4" % (dir_video, year, lon, lat)
else:
    make_video = "ffmpeg -y -r 18 -pattern_type glob -i '%s/*.png' -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p results/analysis/ef/videos/ef_%s_lon_lat_%s_%s.mp4" % (dir_video, year, lon, lat)
os.system(make_video)

# New plot
# 
plt.title('Longitude=%s ; Latitude=%s \nEspectro de energia media no tempo' % (lon, lat))
# plt.plot(selef.f, selef[200], '-k', label='ef com corrente')
# plt.plot(selef_nocur.f, selef_nocur[200], '-.g', label='ef sem corrente')
plt.plot(selef.f, selef[50::].mean('time'), '-k', label='ef com corrente')
plt.plot(selef_nocur.f, selef_nocur[50::].mean('time'), '-.g', label='ef sem corrente')
if sys.argv[3] == 'log':
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(0.04, 1.0)
    plt.ylim(0.0002, 21.0)
    figname = '%s/log_mean_ef_%s_lon_lat_%s_%s.png' % (dir_analysis, year, lon, lat)
else:
    plt.xlim(0.02, 0.8)
    plt.ylim(0, 16)
    figname = '%s/mean_ef_%s_lon_lat_%s_%s.png' % (dir_analysis, year, lon, lat)
plt.xlabel(r'$f$ (Hz)')
plt.ylabel(r'$E(f) (m^2 / Hz)$')
plt.legend()
plt.grid()
# plt.show()
# import pdb; pdb.set_trace()
plt.savefig(figname)
plt.close()