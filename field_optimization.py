from interpolate_unit_convert import Interpolation
from config import *
from read_module import read_json_data
import numpy as np
from scipy.optimize import minimize,Bounds
from well_production import well_production

def fields_optimization(interpolate_obj, fixed_free_vars, well_number):
    print('---- field optimization ----')
    def optimize_qo(QGL):
        global Qliq,free_vars,qo
        free_vars = np.insert(fixed_free_vars, -2, QGL)
        free_vars = np.delete(free_vars,-2,0)
        Qliq = list(well_production(interpolate_obj, free_vars.copy(), well_number))[0]
        WC = fixed_free_vars[2]
        qo = Qliq * (1-WC/100)
        return -qo

    result = minimize(optimize_qo, 100, bounds=Bounds(0, 1400), method=CALCULATE_FIELDS_METHOD)
    QGL = result['x']
    GOR,WC = fixed_free_vars[1],fixed_free_vars[2]
    qw = Qliq * WC/100
    qg = qo*GOR+QGL
    print(f'QGL:{QGL},free variables:{free_vars},qo:{qo},QLiq:{Qliq}')
    return qo,qw,qg,QGL

