import os
from interpolate_unit_convert import Interpolation
from config import *


i = 0 # for iterate J and PR
for data_file in os.listdir(DATA_PATH)[:]:
    free_vars, tpd_res, combinations = read_json_data(DATA_PATH + '/' + data_file)
    # create interpolation object and doing interploation
    interpolate_obj = Interpolation(free_vars,tpd_res)
    interpolate_obj.config_interpolation()
    print('-------------',data_file,'-------------')
    interpolate_obj.well_production(combinations, J[i], PR[i], PB[i], VOGEL_EQUATION[i])
    # un-comment below line to see plots --------
    # interpolate_obj.plot_BHP(input_data, J[i], PR[i], PB[i], VOGEL_EQUATION[i])
    i+=1

