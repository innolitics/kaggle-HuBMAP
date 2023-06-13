import logging, os
import platform, sys
import pandas as pd

get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '3')
print('autoreload 3 enabled')

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT_DIR)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

host_name = platform.node()
print(f'ROOT_DIR: {ROOT_DIR}')
print(f'Host name: {host_name}')