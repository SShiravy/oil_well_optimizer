from config import DATA_DIR,INTERPOLATION_CSV_PATH,WELL_PRODUCTION_CSV_PATH
from interpolate_csv_file import interpolate_df
from well_production import well_production
from field_optimization import fields_optimization
from read_module import read_json_data
from interpolate_unit_convert import Interpolation
import pandas as pd
import numpy as np
import os

# TODO: good prints
# 1- Interpolate six files
# ---- interpolate df (data from csv file , 10 rows of data in this example) ----
# df = pd.read_csv(INTERPOLATION_CSV_PATH)
# print(df)
# RGI_WELLs_dict = interpolate_df(DATA_DIR, df)

# 2- well production
# ----
i = 0  # for csv rows
for data_file in os.listdir(DATA_DIR)[:]:
    free_vars, tpd_res, combinations = read_json_data(DATA_DIR + '/' + data_file)
    # create interpolation object and doing interploation
    interpolate_obj = Interpolation(free_vars, tpd_res)
    interpolate_obj.config_interpolation()
    print('-------------', data_file, '-------------')
    fixed_free_vars = list(pd.read_csv(WELL_PRODUCTION_CSV_PATH).iloc[i])
    fixed_free_vars.append(0)
    well_production(interpolate_obj,np.array(fixed_free_vars),i)
    # fields_optimization(interpolate_obj,np.array(fixed_free_vars),i)
    i+=1


# 3-fields parameters

# fields_params()
