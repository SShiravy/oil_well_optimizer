import numpy as np
import pandas as pd
import os
from read_function import read_json_data
from interpolate_unit_convert import Interpolation

J = [19.73,19.58,19.58,3.71,3.75,3.79] # Sm3/day/bar
PR = [238.88,235.43,235.43,173.38,163.04,152.7] # bara

input_data = [[19.5648,110.05,60,0,0], # WHP,GOR,WC,QGL,Q
              [249.568,275.05,75,4223.2,0],
              [1.01,101.89,100,1408.7,0],
              [87.1912,100.90,24,14.08,0],
              [1.80000,19.790,5,10.22,0]
              ]

def well_production(data_path,freeVariables,input_data):
    i = 0 # for iterate J and PR
    solver_dict = {} # maping file name to its RGIs
    for data_file in os.listdir(data_path):
        free_vars,tpd_res = read_json_data(data_path+'/'+data_file)
        # create interpolation object and doing interploation
        interpolate_obj = Interpolation(free_vars,tpd_res)
        interpolate_obj.config_interpolation()
        print(data_file,'-------------')
        solver_res = interpolate_obj.solver(input_data,J[i],PR[i])
        solver_dict[data_file[:-5]] = solver_res
        print(data_file, '-->', solver_res, '\n')
        i+=1
    return solver_dict
data_path = 'wells data'

df = pd.read_csv('Data_for_Interpolation.csv')
solver_dict = well_production(data_path,df.values[0],input_data)
print(solver_dict,'\n','qo field, qg field and qw field:',sum(solver_dict.values()))
