from config import DATA_DIR,INTERPOLATION_CSV_PATH,WELL_PRODUCTION_CSV_PATH
from well_production import well_production
from field_optimization import fields_optimization
from read_module import read_json_data
from interpolate_unit_convert import Interpolation
import pandas as pd
import numpy as np
import os

# TODO: good prints
if __name__ == '__main__'   :
    # create dataframe for test interpolation
    df = pd.read_csv(INTERPOLATION_CSV_PATH)
    print('dataframe for test interpolation:\n', df)
    i = 0  # for csv rows for task 5
    for data_file in os.listdir(DATA_DIR):
        print('-------------', data_file, '-------------')
        # read json files
        free_vars, tpd_res = read_json_data(DATA_DIR + '/' + data_file)
        # create interpolation object and config interpolation
        interpolate_obj = Interpolation(free_vars, tpd_res)
        interpolate_obj.config_interpolation()
        # 1- Interpolate dataframe
        # ---- interpolate df (data from csv file , 10 rows of data in this example) ----
        list_of_BHPs = interpolate_obj.interpolate(df)
        print('BHP of rows in dataframe:',list_of_BHPs)
        # 2- well production
        fixed_free_vars = list(pd.read_csv(WELL_PRODUCTION_CSV_PATH).iloc[i])
        fixed_free_vars.append(0)
        well_production(interpolate_obj,np.array(fixed_free_vars),i)
        # fields_optimization(interpolate_obj,np.array(fixed_free_vars),i)
        i+=1


    # 3-fields parameters

    # fields_params()
