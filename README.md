## Installation

### Install conda

For packaging management

```
wget https://repo.anaconda.com/archive/Anaconda2-5.3.1-MacOSX-x86_64.pkg
```

### Install environment

conda install xray dask netCDF4 bottleneck

## Hycom dataset

- HYCOM + NCODA Global 1/12° Analysis	Print

- Experiments

| Date Range |	GLBa0.08 ⇣ |	GLBu0.08 ⇣|
| ---------- | ----------- | -----------|
| 2016-04-18 → 2018-11-20 | ✓ Available (expt_91.2) | ✓ Available (expt_91.2) |
| 2014-04-05 → 2016-04-18	| ✓ Available (expt_91.1)	| ✓ Available (expt_91.1) |
| 2013-08-21 → 2014-04-04	| ✓ Available (expt_91.0)	| ✓ Available (expt_91.0) |
| 2011-01-03 → 2013-08-20	| ✓ Available (expt_90.9)	| ~ Available (expt_90.9) |
| 2009-05-07 → 2011-01-02	| ✓ Available (expt_90.8)	| ----------------------- |
| 2008-09-19 → 2009-05-06	| ✓ Available (expt_90.6)	| ----------------------- |

## Example of OpenDap request:

```python
  x = xray.open_dataset('http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_90.6/2008/uvel', decode_times=False)
```
