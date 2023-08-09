from config import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, Bounds
from well_production import well_production


def fields_optimization(interpolate_obj, fixed_free_vars,qgl_max,well_number):
    print('---- field optimization ----')

    def optimize_qo(QGL):
        global Qliq, free_vars, qo
        free_vars = np.insert(fixed_free_vars, -2, QGL)
        free_vars = np.delete(free_vars, -2, 0)
        Qliq = list(well_production(interpolate_obj, free_vars.copy(),Q_MAX[well_number], well_number))[0]
        WC = fixed_free_vars[2]
        qo = Qliq * (1 - WC / 100)
        return -qo

    result = minimize(optimize_qo, 100, bounds=Bounds(0, qgl_max), method=CALCULATE_FIELDS_METHOD)
    print(result)
    QGL = result['x'][0]
    GOR, WC = fixed_free_vars[1], fixed_free_vars[2]
    qw = Qliq * WC / 100
    qg = (qo * GOR + QGL)/1000
    return qo, qw, qg, QGL, Qliq


def plot_qo(fixed_free_vars, interpolate_obj, i,qgl_max):
    """
    using for loop for creating plots
    """
    QO_list = []
    QGL_LIST = np.array(range(30, qgl_max,10))
    for QGL in QGL_LIST:
        free_variables = np.insert(fixed_free_vars, -2, QGL)
        free_variables = np.delete(free_variables, -2, 0)
        Qliq = list(well_production(interpolate_obj, free_variables.copy(),Q_MAX[i], i))[0]
        WC = fixed_free_vars[2]
        qo = Qliq * (1 - WC / 100)
        QO_list.append(qo)
    plt.plot(QGL_LIST, QO_list, color='blue')
    plt.xlabel("Gas Injection Rate, QGL (MSm3/day)")
    plt.ylabel("Oil Production Rate, qo (Sm3/day)")
    plt.savefig(f'images/qo_Well{i + 1}.png')
    plt.figure()
