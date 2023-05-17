import numpy as np
import pandas as pd
import os
from read_function import read_json_data
from interpolate_unit_convert import Interpolation

J = [16.512,16.49,16.49,1.66,1.66,1.663] # STB/d/psi
PR = [238.88,256.11,256.11,209.64,209.64,209.64] # psi

def well_production(data_path,df):
    i = 0 # for iterate J and PR
    for data_file in os.listdir(data_path):
        free_vars,tpd_res = read_json_data(data_path+'/'+data_file)
        # create interpolation object and doing interploation
        interpolate_obj = Interpolation(free_vars,tpd_res)
        interpolate_obj.config_interpolation()
        solver_res = interpolate_obj.solver(df,J[i],PR[i])
        # maping file name to its
        # maping file name to its RGIs
        solver_dict[data_file[:-5]] = solver_res
        print(data_file, '--', solver_res, '\n')
        i+=1

data_path = 'wells data'

df = pd.read_csv('Data_for_Interpolation.csv')
well_production(data_path,df)
