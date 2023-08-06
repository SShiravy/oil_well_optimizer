from read_module import read_json_data
from config import *
from well_production import well_production
from interpolate_unit_convert import Interpolation
import pandas as pd
import numpy as np
import os

i = 0
Q_MAX_list = {
    1: [2356.40],
    2: [2615.34],
    3: [2615.34],
    4: [503.27],
    5: [503.27],
    6: [503.27]
}
for data_file in os.listdir(DATA_DIR):
    print('\n-------------', data_file, '-------------')
    # read json files
    free_vars, tpd_res = read_json_data(DATA_DIR + '/' + data_file)
    # create interpolation object and config interpolation
    interpolate_obj = Interpolation(free_vars, tpd_res)
    interpolate_obj.config_interpolation()
    fixed_free_vars = list(pd.read_csv(WELL_PRODUCTION_CSV_PATH).iloc[i])
    fixed_free_vars.append(0)
    for q_max in Q_MAX_list[i + 1]:
        Q, qw, qo, qg, BHP = well_production(interpolate_obj, np.array(fixed_free_vars), q_max, i)
        print(f'Q max:{q_max}\n'
              f'Q in intersection: {Q} | BHP: {BHP} -->> qo:{qo}, qw:{qw}, qg:{qg}\n'
              f'           =================           ')
    i += 1
