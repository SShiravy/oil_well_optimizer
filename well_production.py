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
        free_vars = np.insert(fixed_free_vars, -1, Q)[:-1]
        BHP_VLP = interpolate_obj.interpolate(free_vars)
        if VOGEL_EQUATION[well_number]:
            q_max = Qmax[well_number]
            BHP_IPR = 0.125 * PR[well_number] * (-1 + (81 - 80 * (Q / q_max)) ** (1 / 2))
        else:
            qb = J[well_number] * (PR[well_number] - PB[well_number])
            q_max = Qmax[well_number]
            BHP_IPR = 0.125 * PB[well_number] * (-1 + (81 - 80 * ((Q - qb) / (q_max - qb))) ** (1 / 2))
        #print(f'freevars:{free_vars}\n---VLP:{BHP_VLP[0]} |||| IPR:{BHP_IPR[0]}')
        return abs(BHP_IPR[0]-BHP_VLP[0])

    # we should specify the bounds parameter to avoid 'out of boundary' error when calculate VLP
    result = minimize(difference,330,bounds=Bounds(64,3000),method=WELL_PRODUCTION_METHOD)
    # q_max = J[well_number] * PR[well_number] / 1.8
    # interpolate_obj.plot_BHP(fixed_free_vars,well_number)
    Q = result['x']
    free_vars = np.insert(fixed_free_vars, -1, Q)[:-1]
    BHP = interpolate_obj.interpolate(free_vars)
    WHP,GOR,WC,QGL,_ = free_vars
    qw = Q * (WC / 100)
    qo = Q - qw  # Q-qw
    qg = qo * GOR + QGL # qo*GOR+GLR*10^3
    print(f'fixed free variables:{fixed_free_vars[:-1]}\nQ_max:{Qmax[well_number]}\nQ in intersection:{Q} and BHP:{BHP} -->> qo:{qo}, qw:{qw}, qg:{qg}')
    return Q

# function to run task 5 on all -----------------------------------------------

# def task_5_all_combinations():
#     i = 0  # iterate J and PR
#     for data_file in os.listdir(DATA_DIR)[:]:
#         free_vars, tpd_res, combinations = read_json_data(DATA_DIR + '/' + data_file)
#         # create interpolation object and doing interploation
#         interpolate_obj = Interpolation(free_vars, tpd_res)
#         interpolate_obj.config_interpolation()
#         print('-------------', data_file, '-------------')
#         # initialization
#         chosen_free_vars = []
#         bigest_Q = 0
#         BHP_bigest_Q = 0
#         qo,qg,qw = 0,0,0
#         any_intersection = False
#         # task 5 :
#         for free_vars in combinations:
#             free_vars = (np.array(free_vars)+unit_convert_intercept)*unit_convert_coefficient
#             result = well_production(interpolate_obj,free_vars,i)
#             # print(free_vars,'\n',result)
#             # if the Q in intersection point is the bigest one then :
#             if result['x'] > bigest_Q:
#                 any_intersection = True
#                 bigest_Q = result['x']
#                 new_free_vars = np.insert(free_vars, -1, bigest_Q)[:-1]
#                 BHP_bigest_Q = interpolate_obj.result(new_free_vars)
#                 chosen_free_vars = free_vars
#                 qw = bigest_Q * (WC / 100)  # Q*(1-WC/100)
#                 qo = bigest_Q - qw  # Q-qw
#                 qg = qo * GOR + QGL * 10 ** 3  # qo*GOR+GLR*10^3
#
#         if any_intersection:
#             print(
#                 f'WHP:{chosen_free_vars[0]}, GOR:{chosen_free_vars[1]},'
#                 f' WC:{chosen_free_vars[2]}, QGL:{chosen_free_vars[3]}, Q:{bigest_Q[0]} ==>> BHP:{BHP_bigest_Q}\n--->> qo:{qo}, qw:{qw}, qg:{qg}\n')
#             # interpolate_obj.plot_BHP([WHP,GOR,WC,QGL,0], J[i], PR[i], PB[i], VOGEL_EQUATION[i])
#         else:
#             print('there is no intersection between IPR & VLP')
#
#     i += 1
