import pandas as pd
import numpy as np
import json
import os

# TODO: remove dir
tpd_files_directory = "I:\oil-well-project\\tpd change to txt" #input('enter directory of tpd files:').replace('\\','/')
json_files_directory = "I:\oil-well-project\program\wells data" #input('enter directory of converted json:').replace('\\','/')


# create all permutation of free vars
def permutation_free_vars(free_vars,var_list,index):
    comb_list = []
    for i in free_vars[0]:
        var_list[index] = i
        if len(free_vars) > 1:
            new_free_vars = free_vars.copy()
            new_free_vars.pop(0)
            comb = permutation_free_vars(new_free_vars,var_list,index+1)
            comb_list.append(comb)
        else:
            comb_list.append(tuple(var_list))
    return comb_list

# create json files
data_dict = {"free variables":
    {
        "Rate values": '',
        "GL rate": '',
        "WC": '',
        "GOR": '',
        "Pressure": ''
    },
    "tpd results": '',
    "combinations": ''
}

for file_name in os.listdir(tpd_files_directory):
    # read all tpd files in the directory then extract free variables and tpd results
    with open(tpd_files_directory+'/'+file_name, 'r') as fp:
        data = fp.readlines()
        index = data.index('# Rate Values\n')
        free_var = data[index:index + 10]
        tpd_res = data[index + 11:]


    # free variables
    free_var = [i.split() for i in free_var]
    free_var = [free_var[i] for i in range(1, 11, 2)]
    for d in range(len(free_var)):
        data_dict['free variables'][list(data_dict['free variables'].keys())[d]] \
            = [float(i.replace(',', '')) for i in free_var[d]]

    # tpd results
    tpd_res = [i.split() for i in tpd_res]
    tpd_res = np.array(tpd_res)[:, 0]
    tpd_res = [float(i.replace(',', '')) for i in tpd_res]
    data_dict['tpd results'] = tpd_res
    # combinations
    comb_list = permutation_free_vars(list(data_dict['free variables'].values())[::-1],[0,0,0,0,0],0)
    comb_array = np.array(comb_list)
    comb_array = comb_array.reshape((6250,5))
    data_dict['combinations'] = comb_array.tolist()
    # save extracted data (data_dict) as json files
    with open(json_files_directory+'/'+file_name[:-3]+'json', 'w') as outfile:
        json.dump(data_dict, outfile,indent=5)
