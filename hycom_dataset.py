import xray
import matplotlib.pyplot as plt
import numpy as np

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
        

if __name__ == "__main__":
        
    xdataset_url = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/uvel'
    ydataset_url = 'http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/vvel'

    x_dataset_instance = HycomDataSet(xdataset_url)
    x_dataset_instance.print_dataset()

    lon = x_dataset_instance.data_set_persist.Longitude[0, :]
    # Normalize lon values
    lon = lon - lon[0].values
    # Set first as -180 and not 0
    lon = lon - 180
    # Find indexes of lon range
    x_indexes = np.where(np.logical_and(lon >= -54, lon <= -30))

    dados = x_dataset_instance.data_set_persist.u[1, 1, 1450,  x_indexes[0]]
    dados.plot()

    import pdb; pdb.set_trace()