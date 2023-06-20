DATA_PATH = 'wells data' # directory of json files

INTERPOLATE_METHOD = "linear" # or cubic

J = [18.76,19.58,19.58,3.71,3.75,3.79] # Sm3/day/bar
PR = [238.882,235.435,235.435,173.382,163.04,152.69791] # bara
PB = [242.33,242.33,242.33,152.698,152.698,152.69797] #
VOGEL_EQUATION = [True, True, True, False, False, True] # vogel or composite

input_data = [[1.01325,101.89,0,0,1500], # WHP,GOR,WC,QGL,Q
              [1.01325,17.90,50,0,1000],
              [1.01325,17.90,25 ,0,1000],
              ]
