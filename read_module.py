import json
import pandas as pd

def read_json_data(file_name):
    '''
    This funciton is to read data in the .json file using json and pandas modules
    :param file_name: directory + name of the data file . json
    :return: free variables and tpd results
    '''
    with open(file_name,'r') as data:
        data_dict = json.load(data)
    free_vars = data_dict["free variables"]
    tpd_res = pd.Series(data_dict["tpd results"])
    return free_vars,tpd_res
