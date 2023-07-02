from interpolate_unit_convert import Interpolation
import pandas as pd
import os
from read_module import read_json_data

def interpolate_df(data_path,df):
    '''
    read data from csv as df, create interpolation obj from free vars and tpd res of wells .json
    and after call .do_interpolation , call the result with df rows as input
    :return: dictionary keys are wells and values are list of RGIs
    '''
    RGI_dict = {}
    for data_file in os.listdir(data_path):
        free_vars,tpd_res = read_json_data(data_path+'/'+data_file)
        # create interpolation object and doing interploation
        interpolate_obj = Interpolation(free_vars,tpd_res)
        interpolate_obj.config_interpolation()
        interpolate_obj.interpolate(df)
        # maping file name to its RGIs
        RGI_dict[data_file[:-5]] = interpolate_obj.well_RGIs
        print(data_file,'--',interpolate_obj.well_RGIs,'\n')

    return RGI_dict




