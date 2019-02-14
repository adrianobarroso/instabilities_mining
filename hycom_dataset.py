import xray
import numpy as np
import pandas as pd
import datetime
import yaml
from tool_scripts import *
from plot import *

class HycomDataSet:
    def __init__(self, xdataset_url, ydataset_url):
        self.xdataset_url = xdataset_url
        self.ydataset_url = ydataset_url
        self.load_dataset()

    def set_lon_lat_array_coordinates(self):
        # import pdb; pdb.set_trace()
        lon_array = self.xdataset_persist.Longitude[0, :].values

        self.lon_array = lon_array - 360
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
        
    def download(self, i1, i2, j1, j2):        
        uvel = self.xdataset_persist.u.isel(X=slice(i1,i2), Y=slice(j1,j2), Depth=0)
        vvel = self.ydataset_persist.v.isel(X=slice(i1,i2), Y=slice(j1,j2), Depth=0)
        ds = xray.Dataset()
        ds['u'] = uvel
        ds['v'] = vvel
        
        import pdb; pdb.set_trace()

    def vel_series_lon_lat(self, lon, lat):
        ix = find_nearest_value_index(self.lon_array, lon)
        iy = find_nearest_value_index(self.lat_array, lat)

        useries = self.xdataset_persist.u.isel(X=ix[1], Y=iy[1], Depth=0)
        vseries = self.ydataset_persist.v.isel(X=ix[1], Y=iy[1], Depth=0)

        return np.sqrt((useries ** 2) + (vseries ** 2))

    def vel(self, i1, i2, j1, j2, dt):
        uvel = self.xdataset_persist.u.isel(X=slice(i1,i2), Y=slice(j1,j2), Depth=0, MT=dt)
        vvel = self.ydataset_persist.v.isel(X=slice(i1,i2), Y=slice(j1,j2), Depth=0, MT=dt)

        return np.sqrt((vvel * vvel) + (uvel * uvel))
        
    def u_v_2d(self, i1, i2, j1, j2, dt):
        uvel = self.xdataset_persist.u.isel(X=slice(i1,i2), Y=slice(j1,j2), Depth=0, MT=dt)
        vvel = self.ydataset_persist.v.isel(X=slice(i1,i2), Y=slice(j1,j2), Depth=0, MT=dt)

        return [uvel, vvel]