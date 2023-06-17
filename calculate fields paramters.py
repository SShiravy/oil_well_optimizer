import numpy as np
import pandas as pd
import os
from read_function import read_json_data
from interpolate_unit_convert import Interpolation
from itertools import permutations

data_path = 'wells data'
df = pd.read_csv('Data_for_Interpolation.csv')
J = [18.76,19.58,19.58,3.71,3.75,3.79] # Sm3/day/bar
PR = [238.88,235.43,235.43,173.38,163.04,152.7] # bara
input_data = [[1.01325,101.89,0,0,1500], # WHP,GOR,WC,QGL,Q
              [1.01325,17.90,50,0,1000],
              [1.01325,17.90,25 ,0,1000],
              ]
i = 0 # for iterate J and PR
field_paramteres_dict = {} # maping file name to its fields param
for data_file in os.listdir(data_path)[:]:
    free_vars,tpd_res = read_json_data(data_path+'/'+data_file)
    # create interpolation object and doing interploation
    interpolate_obj = Interpolation(free_vars,tpd_res)
    interpolate_obj.config_interpolation()
    print(data_file,'-------------')
    field_param = interpolate_obj.fields_params(input_data,J[i],PR[i])
    field_paramteres_dict[data_file[:-5]] = field_param
    i+=1

qo,qg,qw = sum(list(field_paramteres_dict.values()))
print(f'qo:{qo}, qg:{qg}, qw:{qw}')




