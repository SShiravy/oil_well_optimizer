import json
import pandas as pd

def read_json_data(file_name):
    '''
    This funciton is to read data in the .json file using json and pandas modules
    :param file_name: directory + name of the data file . json
    :return: free variables and tpd results
    '''
    with open(file_name,'r') as data:
        data_json_str = json.load(data)
        data_dict = json.loads(data_json_str)
    free_vars = data_dict["free variables"]
    tpd_res = pd.Series(data_dict["tpd results"])
    return free_vars,tpd_res

# print(read_json_data('data_1.json'))
all_data = read_json_data('data_1.json')