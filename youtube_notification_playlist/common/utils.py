"""Utility module.

Commonly used functions and classes are here.
"""

from youtube_notification_playlist.common.env import *


# Short function
ls_all  = lambda path: [path for path in glob(f"{path}/*")]
ls_dir  = lambda path: [path for path in glob(f"{path}/*") if isdir(path)]
ls_file = lambda path: [path for path in glob(f"{path}/*") if isfile(path)]
tprint  = lambda dic: print(tabulate(dic, headers='keys', tablefmt='psql'))  # print with fancy 'psql' format
vars_   = lambda obj: {k: v for k, v in vars(obj).items() if not k.startswith('__')}

def lmap(fn, arr, scheduler=None):
    if scheduler is None:
        return list(map(fn, arr))
    else:
        tasks = [delayed(fn)(e) for e in arr]
        return list(compute(*tasks, scheduler=scheduler))
def lstarmap(fn, *arrs, scheduler=None):
    assert len(np.unqiue(lmap(len, arrs))) == 1, "All parameters should have same length."
    if scheduler is None:
        return list(starmap(fn, arrs))
    else:
        tasks = [delayed(fn)(*es) for es in zip(*arrs)]
        return list(compute(*tasks, scheduler=scheduler))

def yaml2dict(path):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config

# Converter
def str2bool(s):
    if isinstance(s, bool):
        return s
    if s.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif s.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ValueError(f'Invalid input: {s} (type: {type(s)})')
str2dt = lambda s, format="%Y-%m-%d": datetime.datetime.strptime(s, format)
dt2str = lambda dt, format="%Y-%m-%d": dt.strftime(format)


# Metaclass
class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
