from read_module import read_json_data
from config import *
from well_production import well_production
from interpolate_unit_convert import Interpolation
import pandas as pd
import numpy as np
import os

i = 0
whp_test_cases = [14.8, 25, 47]
qgl_for_whp = {
    1: [35.649,41.245,43.764],
    2: [101.325,103.236,150.102],
    3: [46.726,70.922,90.243],
    4: [35.358,55.094,85.014],
    5: [33.002,55.241,91.838],
    6: [29.680,55.807,93.344]
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
    for whp_i in range(len(whp_test_cases)):
        fixed_free_vars[0] = whp_test_cases[whp_i]
        qgl = qgl_for_whp[i+1][whp_i]
        fixed_free_vars[-2] = qgl
        Q, qw, qo, qg, BHP = well_production(interpolate_obj, np.array(fixed_free_vars),Q_MAX[i],i)
        print(f'whp:{fixed_free_vars[0]}\n'
              f'Q in intersection: {Q} | BHP: {BHP} -->> qo:{qo}, qw:{qw}, qg:{qg}\n,free vars:{fixed_free_vars}'
              f'           =================           ')

    i += 1
