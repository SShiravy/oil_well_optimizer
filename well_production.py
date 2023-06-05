import numpy as np
import pandas as pd
import os
from read_function import read_json_data
from interpolate_unit_convert import Interpolation
from itertools import permutations

perm = permutations([1, 2, 3])

J = [18.76,19.58,19.58,3.71,3.75,3.79] # Sm3/day/bar
PR = [238.88,235.43,235.43,173.38,163.04,152.7] # bara
input_data = [[1.01325,101.89,0,0,0], # WHP,GOR,WC,QGL,Q
              [1.01325,17.90,0,0,0],
              [1.01325,17.90,25 ,0,0],
              ]

def well_production(data_path,input_data):
    i = 0 # for iterate J and PR
    for data_file in os.listdir(data_path)[:]:
        free_vars,tpd_res = read_json_data(data_path+'/'+data_file)
        # create interpolation object and doing interploation
        interpolate_obj = Interpolation(free_vars,tpd_res)
        interpolate_obj.config_interpolation()
        print(data_file,'-------------')
        interpolate_obj.solver(input_data,J[i],PR[i])
        interpolate_obj.plot_BHP(input_data,J[i],PR[i])
        i+=1

data_path = 'wells data'

well_production(data_path,input_data)
