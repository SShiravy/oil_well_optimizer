DATA_DIR = 'wells data' # directory of json files
CSV_PATH = 'Data_for_Interpolation.csv'
INTERPOLATE_METHOD = "cubic" # or cubic


J = [18.76,19.58,19.58,3.71,3.75,3.79] # Sm3/day/bar
PR = [238.882,235.435,235.435,173.382,163.04,152.69791] # bara
PB = [242.33,242.33,242.33,152.698,152.698,152.69797] #
VOGEL_EQUATION = [True, True, True, False, False, True] # vogel or composite
WELL_Q_MAX = [2624.158584,2566.751609,2566.751609,'-','-',321.5139327]

#--------------------------->>>> Pressure, GOR, WC, GL rate, Rate values
unit_convert_coefficient = [0.0689476,0.1772,1,28.174,0.158987]
unit_convert_intercept = [14.676,0,0,0,0]
#--------------------------->>>> method for minimize
# Nelder-Mead, L-BFGS-B, TNC, SLSQP, Powell, trust-constr, COBYLA
well_production_method = 'Nelder-Mead'
calculate_field_parameters = 'Nelder-Mead'
