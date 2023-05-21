# This interpolator includes convertion of the units
from scipy import interpolate as irp
import numpy as np
from scipy.optimize import fsolve


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
        self.result = irp.RegularGridInterpolator(points=self.pnts, values=self.reshaped_tpd_res, method="cubic")
        return self.result

    def interpolate(self,df):
        # interpolate each row of df
        self.well_RGIs = self.result(df.values)
        return self.well_RGIs

    def solver(self,data,J,PR):
        Q = 100
        while True:
            data = np.insert(data, -1, Q)[:-1]
            try:
                BHP_VLP = self.result(data)
            except:
                return None
            BHP_IPR = PR-Q/J
            print(data,f'VLP:{BHP_VLP}-IPR:{BHP_IPR}={BHP_VLP-BHP_IPR}')
            Q+=0.1*(BHP_IPR-BHP_VLP)
            if abs(BHP_IPR-BHP_VLP)<1e-6:
                print(data)
                qw = Q*(1-data[2]) # Q*(1-WC)
                qo = Q-qw
                qg = qo*data[1]+data[-2] # qo*GOR+GLR
                return qo,qg,qw











