import xray

class HycomDataSet:

    # Initializer / Instance Attributes
    def __init__(self, xdataset, ydataset):
        self.xdataset = xdataset
        self.ydataset = ydataset

    def print_xdataset(self):
        print(self.xdataset)
  

x = xray.open_dataset('http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/uvel', decode_times=False)
y = xray.open_dataset('http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/vvel', decode_times=False)

print(HycomDataSet(x, y).print_xdataset())
  

