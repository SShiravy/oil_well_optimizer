from read_module import read_json_data
from config import *
from well_production import well_production
from interpolate_unit_convert import Interpolation
import pandas as pd
import numpy as np
import os

i = 0
qw_max_list = {
    1: [840,600,500],
    2: [2615.34],
    3: [2615.34],
    4: [503.27],
    5: [503.27],
    6: [503.27]
}
qgl_for_qw = {
    1: [35,41.265,52.003],
    2: [101.325],
    3: [46.726],
    4: [35.358],
    5: [33.002],
    6: [29.680]
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
    for test_case_i in range(len(qw_max_list[i + 1])):
        qw_max = qw_max_list[i+1][test_case_i]
        q_max = qw_max/(fixed_free_vars[2]/100)
        qgl = qgl_for_qw[i+1][test_case_i]
        fixed_free_vars[-2] = qgl
        Q, qw, qo, qg, BHP = well_production(interpolate_obj, np.array(fixed_free_vars), q_max, i)
        print(f'Q max:{q_max}\n'
              f'Q in intersection: {Q} | BHP: {BHP} -->> qo:{qo}, qw:{qw}, qg:{qg}\n'
              f'           =================           ')
    i += 1
