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

def getuv(wdir):
    wdir_radian = _check_radians(np.radians(wdir), max_radians=4 * np.pi)
    # import pdb; pdb.set_trace()
    u_wave_dir = -np.sin(wdir_radian)
    v_wave_dir = -np.cos(wdir_radian)
    return u_wave_dir, v_wave_dir
    
def _check_radians(value, max_radians=2 * np.pi):
    """Input validation of values that could be in degrees instead of radians.
    Parameters
    ----------
    value : `pint.Quantity`
        The input value to check.
    max_radians : float
        Maximum absolute value of radians before warning.
    Returns
    -------
    `pint.Quantity`
        The input value
    """
    try:
        value = value.to('radians').m
    except AttributeError:
        pass
    if np.greater(np.nanmax(np.abs(value)), max_radians):
        warnings.warn('Input over {} radians. '
                      'Ensure proper units are given.'.format(max_radians))
    return value
