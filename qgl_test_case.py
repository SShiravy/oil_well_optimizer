from read_module import read_json_data
from config import *
from field_optimization import fields_optimization
from interpolate_unit_convert import Interpolation
import pandas as pd
import numpy as np
import os

qgl_test_case = [1400,1000,500]
for qgl_max in qgl_test_case:
    i = 0
    for data_file in os.listdir(DATA_DIR):
        print('\n-------------', data_file, '-------------')
        # read json files
        free_vars, tpd_res = read_json_data(DATA_DIR + '/' + data_file)
        # create interpolation object and config interpolation
        interpolate_obj = Interpolation(free_vars, tpd_res)
        interpolate_obj.config_interpolation()
        fixed_free_vars = list(pd.read_csv(WELL_PRODUCTION_CSV_PATH).iloc[i])
        fixed_free_vars.append(0)
        qo, qw, qg, QGL, Qliq = fields_optimization(interpolate_obj, np.array(fixed_free_vars),qgl_max, i)
        print(f'\nQGL: {QGL}, qo: {qo}, Qliq: {Qliq}\n'
              f'           ==============           ')
        i+=1