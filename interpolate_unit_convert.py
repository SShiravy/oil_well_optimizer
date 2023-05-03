# This interpolator includes convertion of the units

from scipy import interpolate as irp
from read_function import all_data
import numpy as np

class interpolation:
    def __init__(self):
        self.free_vars = all_data[0]
        self.tpd_res = all_data[1]
        self.tpd_res_array = []
        self.new_dim = []

    def dict_convertion(self):
        #The order of unit_list is decided after free variable in well-model from top to bottom. 
        unit_list = ['Rate values', 'GL rate', 'WC', 'GOR', 'Pressure'] #Have to have same length as number of free variables. 
        dict_conv = {}
        for i in range(len(self.free_vars)):
            dict_conv['Free_variable_'+str(i + 1)] = unit_list[i]
        return dict_conv
         
    def convert_points(self, list_2bconverted, f1_add, f2_mult, f3_add):
        list = []
        for i in range(np.size(list_2bconverted)):
            res = (list_2bconverted[i] + f1_add)*f2_mult + f3_add #Unit for converting Liquid rate
            res_2 = round(res, 2)
            list.append(res_2)
        list2arr = np.array(list)
        return list2arr
    
    def get_points(self): 
        l = []
        dict_conversion = self.dict_convertion()
        for i in range(len(self.free_vars)):
            points_dict = []
            df_to_arr = []
            df_to_arr_converted = []
            # TODO: remove dict_conversion
            if dict_conversion['Free_variable_'+str(len(self.free_vars) - i)].lower() == 'rate values':
                points_dict = self.free_vars.get('rate') #Get points from the dictionary they're stored in. Have to get the last element first in this list for the interpolation to be correct
                df_to_arr = np.array(points_dict) #Converts df to numpy array
                df_to_arr_converted = self.convert_points(df_to_arr, 0, 0.158987294928, 0) #Multiplication for rate values unit conversion
                new_arr = df_to_arr_converted.flatten() 
            elif dict_conversion['Free_variable_'+str(len(self.free_vars) - i)].lower() == 'gl rate':
                points_dict = self.free_vars.get('var 4') #Get points from the dictionary they're stored in. Have to get the last element first in this list for the interpolation to be correct
                df_to_arr = np.array(points_dict) #Converts df to numpy array
                df_to_arr_converted = self.convert_points(df_to_arr, 0, 28173.97429124846, 0) #Multiplication for GL rate unit conversion
                new_arr = df_to_arr_converted.flatten() 
            elif dict_conversion['Free_variable_'+str(len(self.free_vars) - i)].lower() == 'wc': #NO conversion for WC
                points_dict = self.free_vars.get('var 3') #Get points from the dictionary they're stored in. Have to get the last element first in this list for the interpolation to be correct
                df_to_arr = np.array(points_dict) #Converts df to numpy array
                new_arr = df_to_arr.flatten()
            elif dict_conversion['Free_variable_'+str(len(self.free_vars) - i)].lower() == 'gor':
                points_dict = self.free_vars.get('var 2') #Get points from the dictionary they're stored in. Have to get the last element first in this list for the interpolation to be correct
                df_to_arr = np.array(points_dict) #Converts df to numpy array
                df_to_arr_converted = self.convert_points(df_to_arr, 0, 0.17810760667903525, 0) #Multiplication for GOR unit conversion
                new_arr = df_to_arr_converted.flatten()
            elif dict_conversion['Free_variable_'+str(len(self.free_vars) - i)].lower() == 'pressure':
                points_dict = self.free_vars.get('var 1') #Get points from the dictionary they're stored in. Have to get the last element first in this list for the interpolation to be correct
                df_to_arr = np.array(points_dict) #Converts df to numpy array
                df_to_arr_converted = self.convert_points(df_to_arr, 0, 0.0689475729, 1) #Multiplication for top node pressure unit conversion (and addition of 1)
                new_arr = df_to_arr_converted.flatten()
            l.append(new_arr)
        return l
    
    def convert_to_tup(self):
        list_input = self.get_points()
        self.convert_tuple = tuple(list_input)
        return self.convert_tuple
        
    def get_data(self): #Get data to the points defined: Columns in TPS Res. This data should be on the regular grid in n dimensions (by def for interpolator)
        self.pnts = self.get_points()
        self.tpd_res_array = self.tpd_res.to_numpy()*0.0689475729 + 1
        #The conversion under only works for col=0 or col=1: If not, the conversion is not done
        # If statement with many cases for new shapes (depending on number of free variables). This code accounts for: 0 <= free variables <= 6 and returns error if above
        if len(self.pnts) == 0:
            return "The number of free variables needs to be at least 1"
        elif len(self.pnts) == 1:
            self.new_dim = np.reshape(self.tpd_res_array, newshape=(len(self.pnts[0])))
            return self.new_dim
        elif len(self.pnts) == 2:
            self.new_dim = np.reshape(self.tpd_res_array, newshape=(len(self.pnts[0]), len(self.pnts[1])))
            return self.new_dim
        elif len(self.pnts) == 3:
            self.new_dim = np.reshape(self.tpd_res_array, newshape=(len(self.pnts[0]), len(self.pnts[1]), len(self.pnts[2])))
            return self.new_dim
        elif len(self.pnts) == 4: 
            self.new_dim = np.reshape(self.tpd_res_array, newshape=(len(self.pnts[0]), len(self.pnts[1]), len(self.pnts[2]), len(self.pnts[3])))
            return self.new_dim
        elif len(self.pnts) == 5:
            self.new_dim = np.reshape(self.tpd_res_array, newshape=(len(self.pnts[0]), len(self.pnts[1]), len(self.pnts[2]), len(self.pnts[3]), len(self.pnts[4])))
            return self.new_dim
        elif len(self.pnts) == 6:
            self.new_dim = np.reshape(self.tpd_res_array, newshape=(len(self.pnts[0]), len(self.pnts[1]), len(self.pnts[2]), len(self.pnts[3]), len(self.pnts[4]), len(self.pnts[5])))
            return self.new_dim
        else:
            return "The number of free variables is not between 1 and 6. The code needs adjustment in the file 'interpolation' and function 'get_data'."

    #Intepolate using linear interpolation 
    def do_interpolation(self):
        self.pnts = self.convert_to_tup()
        self.data = self.get_data()
        self.result = irp.RegularGridInterpolator(points=self.pnts, values=self.data, method="linear")
        return self.result

## Interpolation test
file = interpolation()
res = file.do_interpolation()
test = np.array([119.99, 90.46, 0, 0, 52]) #120, 91, 40, 35003.6, 1418.15
int = res(test)

print(int)
