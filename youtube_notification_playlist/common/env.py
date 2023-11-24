"""Environment module.

Commonly used libraries and options are here.
"""

# Internal library
import sys
import os
from os.path import join, isdir, isfile, exists, basename, dirname, split, abspath
import shutil
from glob import glob
from argparse import ArgumentParser
from importlib import import_module
import datetime
import json
import re
from itertools import product, combinations, permutations, starmap
from functools import reduce, wraps
from time import sleep, perf_counter
from collections import defaultdict
from copy import deepcopy as copy
import warnings
import contextlib
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
import logging


# External library
# import yaml
# import numpy as np
# from tqdm import tqdm, trange
# import pandas as pd
# import joblib
# from switch import Switch
# from tabulate import tabulate
# import numba as nb
# from numba import njit, cuda
# import dask
# from dask import delayed, compute
# import dask.distributed
# import dask.dataframe as dd
# from dask.diagnostics import ProgressBar
#
#
# Plot library
# import matplotlib.pyplot as plt
# from matplotlib.cbook import boxplot_stats
# import seaborn as sns
#
# # Plot options
# """
# # Use korean fonts
# $ sudo apt-get install fonts-nanum* fontconfig
# $ sudo fc-cache -fv
# $ sudo cp /usr/share/fonts/truetype/nanum/Nanum* /opt/conda/envs/caret/lib/python3.8/site-packages/matplotlib/mpl-data/fonts/ttf/
# $ rm -rf /root/.cache/matplotlib/*
# """
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()
# # plt.rc('font', family='NanumGothic')
# plt.rc('font', family='DejaVu Sans')
# plt.rc('axes', unicode_minus=False)
# plt.rc('font', size=20)
# plt.rc('figure', titlesize=40, titleweight='bold')
# plt.style.use('ggplot')
#
#
# # Set options
# np.set_printoptions(suppress=True, precision=6, edgeitems=20, linewidth=100, formatter={"float": lambda x: "{:.3f}".format(x)})
# pd.set_option('display.max_rows', 1000)
# pd.set_option('display.max_columns', 1000)
# pd.set_option('display.max_colwidth', 1000)
# pd.set_option('display.width', 1000)
# pd.set_option('display.float_format', '{:.2f}'.format)


# Warning
warnings.filterwarnings('ignore')

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s [%(pathname)s.%(funcName)s():l%(lineno)d] %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    stream=sys.stdout
)
