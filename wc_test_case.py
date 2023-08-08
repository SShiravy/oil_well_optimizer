from read_module import read_json_data
from config import *
from well_production import well_production
from interpolate_unit_convert import Interpolation
import pandas as pd
import numpy as np
import os

i = 0
wc_test_cases = {
    1: [60,40],
    2: [30,15],
    3: [35,25],
    4: [9,7],
    5: [10,6],
    6: [8,2]
}
qgl_for_wc = {
    1: [55.95,65.82],
    2: [92.28,78.56],
    3: [44.8,32.45],
    4: [36.17,36.99],
    5: [33.36,35.006],
    6: [29.75,30.28]
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
    for wc_i in range(len(wc_test_cases[i + 1])):
        wc = wc_test_cases[i + 1][wc_i]
        fixed_free_vars[2] = wc
        qgl = qgl_for_wc[i + 1][wc_i]
        fixed_free_vars[-2] = qgl
        Q, qw, qo, qg, BHP = well_production(interpolate_obj, np.array(fixed_free_vars), Q_MAX[i], i)
        print(f'wc:{wc},qgl:{qgl}, Q in intersection: {Q} | BHP: {BHP} -->> qo:{qo}, qw:{qw}, qg:{qg}\n'
              f'           =================           ')
    i += 1
