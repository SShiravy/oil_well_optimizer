import time
from interpolate_unit_convert import Interpolation
import pandas as pd
import os
from read_function import read_json_data

def interpolate_all_wells():
    '''
    read data from csv as df, create interpolation obj from free vars and tpd res of wells .json
    and after call .do_interpolation , call the result with df rows as input
    :return: dictionary keys are wells and values are list of RGIs
    '''
    df = pd.read_csv('Data_for_Interpolation.csv')
    print(df)
    data_path = 'wells data'
    RGI_dict = {}
    for data_file in os.listdir(data_path):
        free_vars,tpd_res = read_json_data(data_path+'/'+data_file)
        interpolate_obj = Interpolation(free_vars,tpd_res)
        result = interpolate_obj.do_interpolation()
        RGI_well = []
        print(data_file,'--',free_vars,'========================================')
        for row in df.values.tolist():
            # (WHP, GOR, WC, GLR, LR)
            RGI = result(row[::-1])
            RGI_well.append(RGI)

        print(RGI_well,'\n')
        # file name to all RGIs , ex: Well1 : [....]
        RGI_dict[data_file[:-5]] = RGI_well

    return RGI_dict

RGI_WELLs_dict = interpolate_all_wells()
print('RGI for each well with given data is:\n', RGI_WELLs_dict)

#
# Pressure
# GOR
# WC
# GL rate
