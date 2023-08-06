from read_module import read_json_data
from config import *
from well_production import well_production
from interpolate_unit_convert import Interpolation
import pandas as pd
import numpy as np
import os

i = 0
whp_test_cases = [14.8, 25, 36, 47]
for data_file in os.listdir(DATA_DIR):
    print('\n-------------', data_file, '-------------')
    # read json files
    free_vars, tpd_res = read_json_data(DATA_DIR + '/' + data_file)
    # create interpolation object and config interpolation
    interpolate_obj = Interpolation(free_vars, tpd_res)
    interpolate_obj.config_interpolation()
    fixed_free_vars = list(pd.read_csv(WELL_PRODUCTION_CSV_PATH).iloc[i])
    fixed_free_vars.append(0)
    for whp in whp_test_cases:
        fixed_free_vars[0] = whp
        Q, qw, qo, qg, BHP = well_production(interpolate_obj, np.array(fixed_free_vars), i)
        print(f'whp:{fixed_free_vars[0]}\n'
              f'Q in intersection: {Q} | BHP: {BHP} -->> qo:{qo}, qw:{qw}, qg:{qg}\n'
              f'           =================           ')

    i += 1
