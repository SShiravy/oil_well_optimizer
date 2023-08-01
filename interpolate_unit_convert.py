# This interpolator includes convertion of the units
from scipy import interpolate as irp
import numpy as np

from config import *


class Interpolation:
    def __init__(self, free_vars, tpd_res):
        self.free_vars = free_vars
        self.tpd_res = tpd_res
        self.tpd_res_unit_converted = []
        self.reshaped_tpd_res = None
        self.pnts = None
        self.interpolate = None

    def convert_points(self, list_of_free_var, alpha, beta):
        list_converted = []
        for i in range(np.size(list_of_free_var)):
            res = (list_of_free_var[i] + alpha) * beta  # Unit for converting Liquid rate
            res_2 = round(res, 2)
            list_converted.append(res_2)
        array_converted = np.array(list_converted)
        return array_converted

    def get_points(self):
        # create a tuple of unit converted points and
        rate_values = self.convert_points(self.free_vars.get('Rate values'), 0, 0.158987).flatten()
        gl_rate = self.convert_points(self.free_vars.get('GL rate'), 0, 28.174).flatten()
        wc = self.convert_points(self.free_vars.get('WC'), 0, 1).flatten()
        gor = self.convert_points(self.free_vars.get('GOR'), 0, 0.1772).flatten()
        pressure = self.convert_points(self.free_vars.get('Pressure'), 14.696, 0.0689476).flatten()
        self.pnts = (pressure, gor, wc, gl_rate, rate_values)

    def get_data(self):
        """
        Get reshaped_tpd_res to the points defined: Columns in TPS Res. This reshaped_tpd_res should be on the
        regular grid in n dimensions (by def for interpolator)
        """
        self.tpd_res_unit_converted = (self.tpd_res.to_numpy() + 14.696) * 0.06894
        # The conversion under only works for col=0
        self.reshaped_tpd_res = np.reshape(self.tpd_res_unit_converted, newshape=(
            len(self.pnts[0]), len(self.pnts[1]), len(self.pnts[2]), len(self.pnts[3]), len(self.pnts[4])))

    def config_interpolation(self):
        self.get_points()
        self.get_data()
        self.interpolate = irp.RegularGridInterpolator(points=self.pnts, values=self.reshaped_tpd_res,
                                                       method=INTERPOLATE_METHOD)
        return self.interpolate
