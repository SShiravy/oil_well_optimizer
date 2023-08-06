from config import DATA_DIR, INTERPOLATION_CSV_PATH, WELL_PRODUCTION_CSV_PATH, Q_MAX, TOTAL_QGL
from well_production import well_production, plot_ipr_vlp
from field_optimization import fields_optimization, plot_qo
from read_module import read_json_data
from interpolate_unit_convert import Interpolation
import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

# TODO: good prints
if __name__ == '__main__':
    # create dataframe for test interpolation
    df = pd.read_csv(INTERPOLATION_CSV_PATH)
    print('dataframe for test interpolation:\n', df)
    qo_field, qw_field, qg_field, QGL_field = 0, 0, 0, 0
    i = 0  # for csv rows for task 5
    for data_file in os.listdir(DATA_DIR):
        print('\n-------------', data_file, '-------------')
        # read json files
        free_vars, tpd_res = read_json_data(DATA_DIR + '/' + data_file)
        # create interpolation object and config interpolation
        interpolate_obj = Interpolation(free_vars, tpd_res)
        interpolate_obj.config_interpolation()
        # 1- Interpolate dataframe
        # ---- interpolate df (data from csv file , 10 rows of data in this example) ----
        list_of_BHPs = interpolate_obj.interpolate(df)
        print(f'BHP of rows in dataframe:\n{list_of_BHPs}')
        # 2- well production
        fixed_free_vars = list(pd.read_csv(WELL_PRODUCTION_CSV_PATH).iloc[i])
        fixed_free_vars.append(0)
        Q, qw, qo, qg, BHP = well_production(interpolate_obj, np.array(fixed_free_vars),Q_MAX[i], i)
        print(f'fixed free variables:{fixed_free_vars[:-1]}\nQ_max:{Q_MAX[i]}\n'
              f'Q in intersection: {Q} | BHP: {BHP} -->> qo:{qo}, qw:{qw}, qg:{qg}')
        plot_ipr_vlp(interpolate_obj, fixed_free_vars, i)
        # 3-fields parameters
        qo, qw, qg, QGL, Qliq = fields_optimization(interpolate_obj, np.array(fixed_free_vars),1400, i)
        print(f'\nQGL: {QGL}, qo: {qo}, Qliq: {Qliq}')
        plot_qo(fixed_free_vars, interpolate_obj, i, 1400)
        # summation for fields parameters
        qo_field += qo
        qw_field += qw
        qg_field += qg
        QGL_field += QGL
        i += 1

    print(f'------------------------------\n'
          f'qo field:{qo_field},qw field:{qw_field},'
          f'qg field:{qg_field},QGL field:{QGL_field},total QGL:{TOTAL_QGL}')
