from config import *
import numpy as np
from scipy.optimize import minimize, Bounds
import matplotlib.pyplot as plt


def well_production(interpolate_obj, fixed_free_vars, well_number):
    """
    this method calculate qo,qw,qg using given inputs for each well
    where we have biggest Q of the intersection between IPR and VLP
    for task 5
    """
    def difference(Q):
        global BHP_VLP
        free_vars = np.insert(fixed_free_vars, -1, Q)[:-1]
        BHP_VLP = interpolate_obj.interpolate(free_vars)
        q_max = Q_MAX[well_number]
        if VOGEL_EQUATION[well_number]:
            BHP_IPR = 0.125 * PR[well_number] * (-1 + (81 - 80 * (Q / q_max)) ** (1 / 2))
        else:
            qb = J[well_number] * (PR[well_number] - PB[well_number])
            BHP_IPR = 0.125 * PB[well_number] * (-1 + (81 - 80 * ((Q - qb) / (q_max - qb))) ** (1 / 2))
        return abs(BHP_IPR[0] - BHP_VLP[0])

    # we should specify the bounds parameter to avoid 'out of boundary' error when calculate VLP
    result = minimize(difference, Q_initial[well_number], bounds=Bounds(63, 3200), method=WELL_PRODUCTION_METHOD)
    Q = result['x'][0]
    _, GOR, WC, QGL, _ = fixed_free_vars
    qw = Q * (WC / 100)
    qo = Q - qw  # Q-qw
    qg = (qo * GOR + QGL) / 1000
    return Q, qw, qo, qg, BHP_VLP[0]


def plot_ipr_vlp(interpolate_obj, free_vars, i):
    """
    using for loop for creating plots
    """
    vlp, ipr = [], []
    Q_list = np.array(range(64, 3000, 15))
    for Q in Q_list:
        free_vars = np.insert(free_vars, -1, Q)[:-1]
        vlp.append(interpolate_obj.interpolate(free_vars)[0])
        if VOGEL_EQUATION[i]:
            q_max = Q_MAX[i]
            ipr_bhp = 0.125 * PR[i] * (-1 + (81 - 80 * (Q / q_max)) ** (1 / 2))
        else:
            qb = J[i] * (PR[i] - PB[i])
            q_max = Q_MAX[i]
            ipr_bhp = 0.125 * PB[i] * (-1 + (81 - 80 * ((Q - qb) / (q_max - qb))) ** (1 / 2))

        ipr.append(ipr_bhp) if ipr_bhp > 0 else ipr.append(0)

    plt.plot(Q_list, vlp, color='blue')
    plt.plot(Q_list, ipr, color='red')
    plt.xlabel("Liquid Rate")
    plt.ylabel("Flowing Bottom Hole Pressure")
    plt.savefig(f'images/IPR_VLP-Well{i + 1}.png')
    plt.figure()