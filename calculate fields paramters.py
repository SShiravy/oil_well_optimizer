import os
from read_module import read_json_data
from interpolate_unit_convert import Interpolation
from config import *


i = 0 # for iterate J and PR
field_paramteres_dict = {} # maping file name to its fields param
for data_file in os.listdir(DATA_PATH)[:]:
    free_vars, tpd_res, combinations = read_json_data(DATA_PATH + '/' + data_file)
    # create interpolation object and doing interploation
    interpolate_obj = Interpolation(free_vars,tpd_res)
    interpolate_obj.config_interpolation()
    print('-------------',data_file,'-------------')
    field_param = interpolate_obj.fields_params(combinations, J[i], PR[i], PB[i], VOGEL_EQUATION[i])
    field_paramteres_dict[data_file[:-5]] = field_param
    i+=1

qo_field,qg_field,qw_field = sum(list(field_paramteres_dict.values()))
print(f'qo field:{qo_field}, qg field:{qg_field}, qw field:{qw_field}')
