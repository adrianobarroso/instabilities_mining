import numpy as np
import yaml

def array_stations(data_stations):
    array_lon = []
    array_lat = []
    
    for project in data_stations:
        for station in data_stations[project]:
            lon = data_stations[project][station]['lon']
            lat = data_stations[project][station]['lat']
            
            array_lon = array_lon + [lon]
            array_lat = array_lat + [lat]
    
    return [array_lon, array_lat]


def find_nearest_value_index(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return [array[idx], idx]
    
def get_yaml(arg):
    yaml_file=arg
    file = open(yaml_file).read()
    return yaml.load(file)