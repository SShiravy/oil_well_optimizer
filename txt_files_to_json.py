import numpy as np
import json
import os

txt_files_directory = input('enter directory of txt files:').replace('\\', '/')
json_files_directory = input('enter directory of converted json:').replace('\\', '/')

# create json files
data_dict = {
    "free variables":
        {
            "Rate values": '',
            "QGL": '',
            "WC": '',
            "GOR": '',
            "Pressure": ''
        },
    "tpd results": '',
}

for file_name in os.listdir(txt_files_directory):
    # read all tpd files in the directory then extract free variables and tpd results
    with open(txt_files_directory + '/' + file_name, 'r') as fp:
        data = fp.readlines()
        index = data.index('# Rate Values\n')
        free_var = data[index:index + 10]
        tpd_res = data[index + 11:]
    # free variables
    free_var = [i.split() for i in free_var]
    free_var = [free_var[i] for i in range(1, 11, 2)]
    for d in range(len(free_var)):
        choosen_free_var = list(data_dict['free variables'].keys())[d]
        data_dict['free variables'][choosen_free_var] \
            = [float(i.replace(',', '')) for i in free_var[d]]
    # tpd results
    tpd_res = [i.split() for i in tpd_res]
    tpd_res = np.array(tpd_res)[:, 0]
    tpd_res = [float(i.replace(',', '')) for i in tpd_res]
    data_dict['tpd results'] = tpd_res
    # create json file
    with open(json_files_directory + '/' + file_name[:-3] + 'json', 'w') as outfile:
        json.dump(data_dict, outfile, indent=5)