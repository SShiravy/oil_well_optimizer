from interpolate_unit_convert import Interpolation
import pandas as pd
import os
from read_function import read_json_data

def interpolate_all_wells(data_path,df):
    '''
    read data from csv as df, create interpolation obj from free vars and tpd res of wells .json
    and after call .do_interpolation , call the result with df rows as input
    :return: dictionary keys are wells and values are list of RGIs
    '''
    RGI_dict = {}
    wells_interpolate_obj = [] # for solver function in next step we save all interpolate objects
    for data_file in os.listdir(data_path):
        free_vars,tpd_res = read_json_data(data_path+'/'+data_file)
        # create interpolation object and doing interploation
        interpolate_obj = Interpolation(free_vars,tpd_res)
        result = interpolate_obj.do_interpolation()
        # interpolate each row of df
        RGI_well = []
        print(data_file,'--',free_vars)
        for row in df.values.tolist():
            # (Q,QGL,WC,GOR,WHP)
            wells_interpolate_obj.append(result)
            RGI = result(row)
            RGI_well.append(RGI)

        print(RGI_well,'\n')
        # file name to all RGIs , ex: Well1 : [....]
        RGI_dict[data_file[:-5]] = RGI_well

    return RGI_dict,wells_interpolate_obj

# -----------------------------------------------------------------------------------
data_path = 'wells data'

df = pd.read_csv('Data_for_Interpolation.csv')
print(df)
# run function to interpolate df (data from csv file , 10 rows of data in this example)

RGI_WELLs_dict,wells_interpolate_obj = interpolate_all_wells(data_path,df)
