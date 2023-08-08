from scipy.optimize import minimize
import os
import numpy as np
import pandas as pd
from config import *
from read_module import read_json_data
from interpolate_unit_convert import Interpolation
from well_production import well_production

FIXED_FREE_VARS_LIST = []
INTERPOLATION_OBJ_LIST = []
i=0
for data_file in os.listdir(DATA_DIR):
    print('\n-------------', data_file, '-------------')
    # read json files
    free_vars, tpd_res = read_json_data(DATA_DIR + '/' + data_file)
    # create interpolation object and config interpolation
    interpolate_obj = Interpolation(free_vars, tpd_res)
    interpolate_obj.config_interpolation()
    fixed_free_vars = list(pd.read_csv(WELL_PRODUCTION_CSV_PATH).iloc[i])
    fixed_free_vars.append(0)
    FIXED_FREE_VARS_LIST.append(fixed_free_vars)
    INTERPOLATION_OBJ_LIST.append(interpolate_obj)
    i+=1
print('END',FIXED_FREE_VARS_LIST)

def solution2(fixed_free_vars,interpolate_obj):
    print('---- field optimization ----')
    def optimize_qo(QGL_list):
        qo_sum = 0
        for well_number in range(6):
            free_vars = np.insert(fixed_free_vars[well_number], -2, QGL_list[well_number])
            free_vars = np.delete(free_vars, -2, 0)
            Qliq = list(well_production(interpolate_obj[well_number], free_vars.copy(),Q_MAX[well_number], well_number))[0]
            WC = fixed_free_vars[well_number][2]
            qo_sum += Qliq * (1 - WC / 100)
        return -qo_sum
    result = minimize(optimize_qo, [100,100,100,100,100,100], method=CALCULATE_FIELDS_METHOD)
    print(result)
    QGL = result['x'][0]

solution2(FIXED_FREE_VARS_LIST,INTERPOLATION_OBJ_LIST)