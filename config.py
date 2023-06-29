DATA_PATH = 'wells data' # directory of json files

INTERPOLATE_METHOD = "cubic" # or cubic


J = [18.76,19.58,19.58,3.71,3.75,3.79] # Sm3/day/bar
PR = [238.882,235.435,235.435,173.382,163.04,152.69791] # bara
PB = [242.33,242.33,242.33,152.698,152.698,152.69797] #
VOGEL_EQUATION = [True, True, True, False, False, True] # vogel or composite

#--------------------------->>>> Pressure, GOR, WC, GL rate, Rate values
unit_convert_coefficient = [0.0689475729,0.17810760667903525,1,28.17397429124846,0.158987294928]
unit_convert_intercept = [14.676,0,0,0,0]
