DATA_DIR = 'wells data'  # directory of json files
INTERPOLATION_CSV_PATH = 'Data_for_Interpolation.csv'
WELL_PRODUCTION_CSV_PATH = 'Data_for_well_production.csv'
INTERPOLATE_METHOD = "cubic"  # or cubic,pchip

J = [19.77, 19.73, 19.72, 3.53, 3.53, 3.53]  # Sm3/day/bar
PR = [238.882, 256.119, 256.119, 209.649, 209.649, 209.649]  # bara
PB = [242.33, 242.33, 242.33, 152.698, 152.698, 152.698]  #
VOGEL_EQUATION = [True, False, False, False, False, False]  # vogel or composite
Q_MAX = [2370.73, 2275.04, 2275.04, 499.9205, 499.9205, 499.9205]
Q_initial = [1000, 1000, 1000, 100, 100, 100]
TOTAL_QGL = 1408.69
# GAP: 2356.40,2615.34,2615.34,503.27,503.27,503.27
# --------------------------->>>> Pressure, GOR, WC, QGL, Rate values
unit_convert_coefficient = [0.0689476, 0.1772, 1, 28.174, 0.158987]
unit_convert_intercept = [14.696, 0, 0, 0, 0]
# --------------------------->>>> method for minimize
# Nelder-Mead, L-BFGS-B, TNC, SLSQP, Powell, trust-constr, COBYLA
WELL_PRODUCTION_METHOD = 'Nelder-Mead'
CALCULATE_FIELDS_METHOD = 'Nelder-Mead'
