import os
from interpolate_unit_convert import Interpolation
from config import *
from read_module import read_json_data
import numpy as np
from scipy.optimize import minimize,Bounds


def well_production(interpolate_obj, fixed_free_vars, well_number):
    '''
    this method calculate qo,qw,qg using given inputs for each well
    where we have bigest Q of the intersection between IPR and VLP
    for task 5
    '''
    def difference(Q):
        global BHP_VLP
        free_vars = np.insert(fixed_free_vars, -1, Q)[:-1]
        BHP_VLP = interpolate_obj.interpolate(free_vars)
        if VOGEL_EQUATION[well_number]:
            q_max = Q_MAX[well_number]
            BHP_IPR = 0.125 * PR[well_number] * (-1 + (81 - 80 * (Q / q_max)) ** (1 / 2))
        else:
            qb = J[well_number] * (PR[well_number] - PB[well_number])
            q_max = Q_MAX[well_number]
            BHP_IPR = 0.125 * PB[well_number] * (-1 + (81 - 80 * ((Q - qb) / (q_max - qb))) ** (1 / 2))
        #print(f'freevars:{free_vars}\n---VLP:{BHP_VLP[0]} |||| IPR:{BHP_IPR[0]}')
        return abs(BHP_IPR[0]-BHP_VLP[0])

    # we should specify the bounds parameter to avoid 'out of boundary' error when calculate VLP
    result = minimize(difference,Q_initial[well_number],bounds=Bounds(64,3000),method=WELL_PRODUCTION_METHOD)
    Q = result['x']
    _,GOR,WC,QGL,_ = fixed_free_vars
    qw = Q * (WC / 100)
    qo = Q - qw  # Q-qw
    qg = (qo * GOR + QGL)/1000
    return Q,qw,qo,qg,BHP_VLP