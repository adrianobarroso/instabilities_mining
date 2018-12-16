import xray

class HycomDataSet:

    # Initializer / Instance Attributes
    def __init__(self, x_dataset, y_dataset):
        self.x_dataset = x_dataset
        self.y_dataset = y_dataset

    # def get_

x = xray.open_dataset('http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/uvel', decode_times=False)
y = xray.open_dataset('http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/vvel', decode_times=False)
