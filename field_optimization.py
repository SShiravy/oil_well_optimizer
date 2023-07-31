import os
from interpolate_unit_convert import Interpolation
from config import *
from read_module import read_json_data
import numpy as np
from scipy.optimize import minimize,Bounds
from well_production import well_production

def fields_optimization(interpolate_obj, fixed_free_vars, well_number):
    print('---- field optimization ----')
    def optimize_qo(QGL):
        QGL = QGL*28.174
        global Qliq,free_vars,qo
        free_vars = np.insert(fixed_free_vars, -2, QGL)
        free_vars = np.delete(free_vars,-2,0)
        print(QGL,free_vars)
        # print(free_vars)
        Qliq = list(well_production(interpolate_obj, free_vars.copy(), well_number))[0]
        WC = fixed_free_vars[2]
        qo = Qliq * (1-WC/100)
        #print(f'qliq{Qliq},qo{qo},QGL{QGL}')
        return -Qliq

    result = minimize(optimize_qo, 20, bounds=Bounds(0, 500), method=CALCULATE_FIELDS_METHOD)
    print(result)
    QGL = result['x']
    print(f'QGL:{QGL},free variables:{free_vars},qo:{qo}')

