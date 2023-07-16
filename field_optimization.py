import os
from interpolate_unit_convert import Interpolation
from config import *
from read_module import read_json_data
import numpy as np
from scipy.optimize import minimize,Bounds
from well_production import well_production

def fields_optimization(interpolate_obj, fixed_free_vars, well_number):
    def optimize_qo(QGL):
        QGL = QGL*28.174
        free_vars = np.insert(fixed_free_vars, -2, QGL)
        free_vars = np.delete(free_vars,-2,0)
        print(free_vars)
        Qliq = well_production(interpolate_obj, free_vars, well_number)
        WC = fixed_free_vars[2]
        qo = (Qliq * (1-WC/100))
        print(f'qliq{Qliq},qo{qo},QGL{QGL}')
        return -qo[0]

    result = minimize(optimize_qo, 250, bounds=Bounds(0, 500), method=CALCULATE_FIELDS_METHOD)
    # 11.
    QGL = result['x']
    free_vars = np.insert(fixed_free_vars, -2, QGL)
    free_vars = np.delete(free_vars, -2, 0)
    Qliq = well_production(interpolate_obj, free_vars, well_number)
    print()
    print(result['x'],(Qliq * (1-fixed_free_vars[2]/100)))

