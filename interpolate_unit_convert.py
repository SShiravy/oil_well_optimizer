# This interpolator includes convertion of the units
from scipy import interpolate as irp
import numpy as np
from scipy.optimize import minimize,fsolve
import matplotlib.pyplot as plt

class Interpolation:
    def __init__(self,free_vars,tpd_res):
        self.free_vars =free_vars
        self.tpd_res = tpd_res
        self.tpd_res_unit_converted = []
        self.reshaped_tpd_res = None
        self.pnts = None
        self.result = None
        self.well_RGIs = []

    # unit_list = ['Rate values', 'GL rate', 'WC', 'GOR', 'Pressure'] #Have to have same length as number of free variables.
    def convert_points(self, list_2bconverted, alpha, beta):
        list = []
        for i in range(np.size(list_2bconverted)):
            res = (list_2bconverted[i] + alpha) * beta  # Unit for converting Liquid rate
            res_2 = round(res, 2)
            list.append(res_2)
        list2arr = np.array(list)
        return list2arr

    def get_points(self):
        points = []
        for var in list(self.free_vars.keys())[::-1]:
            if var == 'Rate values':
                points_dict = self.free_vars.get(
                    'Rate values')  # Get points from the dictionary they're stored in. Have to get the last element first in this list for the interpolation to be correct
                df_to_arr = np.array(points_dict)  # Converts df to numpy array
                df_to_arr_converted = self.convert_points(df_to_arr, 0, 0.158987294928)
                                                           # Multiplication for rate values unit conversion
                new_arr = df_to_arr_converted.flatten()
            elif var == 'GL rate':
                points_dict = self.free_vars.get(
                    'GL rate')  # Get points from the dictionary they're stored in. Have to get the last element first in this list for the interpolation to be correct
                df_to_arr = np.array(points_dict)  # Converts df to numpy array
                df_to_arr_converted = self.convert_points(df_to_arr, 0, 28.17397429124846)
                                                           # Multiplication for GL rate unit conversion
                new_arr = df_to_arr_converted.flatten()
            elif var == 'WC':  # NO conversion for WC
                points_dict = self.free_vars.get(
                    'WC')  # Get points from the dictionary they're stored in. Have to get the last element first in this list for the interpolation to be correct
                df_to_arr = np.array(points_dict)  # Converts df to numpy array
                new_arr = df_to_arr.flatten()
            elif var == 'GOR':
                points_dict = self.free_vars.get(
                    'GOR')  # Get points from the dictionary they're stored in. Have to get the last element first in this list for the interpolation to be correct
                df_to_arr = np.array(points_dict)  # Converts df to numpy array
                df_to_arr_converted = self.convert_points(df_to_arr, 0, 0.17810760667903525)
                                                            # Multiplication for GOR unit conversion
                new_arr = df_to_arr_converted.flatten()
            elif var == 'Pressure':
                points_dict = self.free_vars.get(
                    'Pressure')  # Get points from the dictionary they're stored in. Have to get the last element first in this list for the interpolation to be correct
                df_to_arr = np.array(points_dict)  # Converts df to numpy array
                df_to_arr_converted = self.convert_points(df_to_arr, 14.696, 0.0689475729)
                                                            # Multiplication for top node pressure unit conversion (and addition of 1)
                new_arr = df_to_arr_converted.flatten()
            points.append(new_arr)
        self.pnts = tuple(points)

    def get_data(self):  # Get reshaped_tpd_res to the points defined: Columns in TPS Res. This reshaped_tpd_res should be on the regular grid in n dimensions (by def for interpolator)
        self.tpd_res_unit_converted = (self.tpd_res.to_numpy() + 14.696) * 0.06894
        # The conversion under only works for col=0
        self.reshaped_tpd_res = np.reshape(self.tpd_res_unit_converted, newshape=(
        len(self.pnts[0]), len(self.pnts[1]), len(self.pnts[2]), len(self.pnts[3]), len(self.pnts[4])))


    # Intepolate using linear interpolation
    def config_interpolation(self):
        self.get_points()
        self.get_data()
        self.result = irp.RegularGridInterpolator(points=self.pnts, values=self.reshaped_tpd_res, method="linear")
        return self.result

    def interpolate(self,df):
        # interpolate each row of df
        self.well_RGIs = self.result(df.values)
        return self.well_RGIs

    def solver(self,input_data,J,PR):
        qw,qo,qg = 0,0,0
        Q = 1000
        bigest_Q = 0
        for free_vars in input_data:
            free_vars = np.insert(free_vars, -1, Q)[:-1]
            print('free variables:',free_vars)
            def difference(Q):
                BHP_VLP = self.result(free_vars)
                BHP_IPR = PR - Q / J
                return abs(BHP_IPR[0]-BHP_VLP[0])

            result = minimize(difference,Q,method='BFGS')
            print(f'Q: {result["x"]} --> BHP: {self.result(np.insert(free_vars, -1, result["x"])[:-1])}',result)
            #
            # if result['x'][0]>bigest_Q and free_vars[2]!=0:
            #     bigest_Q = result['x'][0]
            #     qw = bigest_Q * (1 - free_vars[2] / 100)  # Q*(1-WC/100)
            #     qo = bigest_Q - qw
            #     qg = qo * free_vars[1] + free_vars[-2] * 10 ** 3  # qo*GOR+GLR*10^3

        # return np.array([round(qo,2),round(qg,2),round(qw,2)]) , bigest_Q

    def plot_BHP(self,input_data,J,PR):
        for free_vars in input_data:
            BHP_VLP,BHP_IPR=[],[]
            Q_list = np.array(range(300, 3000))
            for Q in Q_list:
                free_vars = np.insert(free_vars, -1, Q)[:-1]
                BHP_VLP.append(self.result(free_vars)[0])
                BHP_IPR.append(PR - Q / J)

            print('free variables:', free_vars,'\n')
            print(f'1--IPR:{np.array(BHP_IPR[1022])}\nQ:{Q_list[1022]}\nVLP:{np.array(BHP_VLP[1022])}')
            print(f'2--IPR:{np.array(BHP_IPR[74])}\nQ:{Q_list[74]}\nVLP:{np.array(BHP_VLP[74])}')
            plt.plot(Q_list, BHP_VLP, color='blue')
            plt.plot(Q_list, BHP_IPR, color='red')
            plt.show()
