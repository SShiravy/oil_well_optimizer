import pandas as pd
import numpy as np
import json
# with open('DHG2WH.txt', 'r') as fp:
#     data = fp.readlines()[76:142]
#     print(len(data))
#
# data = [i.split()[1:] for i in data]
# columns = ['Type','Label','Rate Multiplier','Measured Depth(m)','True Vertical Depth(m)','Pipe Length(m)','Tubing Inside Diameter(inches)','Tubing Inside Roughness(inches)']
#
# data.insert(0,columns)
# print(data)
#
# np.savetxt("Equipment Summary.csv",
#                data,
#            delimiter =", ",  # Set the delimiter as a comma followed by a space
#            fmt ='% s')  # Set the format of the data as string
#
# data = pd.read_csv('Equipment Summary.csv')
# print(data)
#
# with open('DHG2WH.txt', 'r') as fp:
#     data = fp.readlines()[215:]
#     print(len(data))
#
# data = [i.split() for i in data]
# # print([len(i) for i in data])
# # print(data)
# data.insert(0,[0]*len(data[1]))
# data = np.array(data)
# data = pd.Series(data[:,0])
# data.to_csv("free variables")
# np.savetxt("4 Variable TPD Results.csv",
#                data,
#            delimiter =", ",  # Set the delimiter as a comma followed by a space
#            fmt ='% s')  # Set the format of the data as string
#
# data = pd.read_csv('4 Variable TPD Results.csv')
# print(data,pd.read_csv('free variables'))
# #------------------------------
#
# from read_model import Read_Model
#
# files = Read_Model('','4 Variable TPD Results.csv','Equipment Summary.csv')
# files.read_all()
#



with open('tpd change to txt/Well6.txt', 'r') as fp:
    data = fp.readlines()
    tpd_res = data[148:]
    free_var = data[137:147]

data_dict = {"free variables":
                {
                "rate":'',
                "var 4":'',
                "var 3":'',
                "var 2":'',
                "var 1":''
                },
             "tpd results":''
             }
# free var
free_var = [i.split() for i in free_var]
free_var = [free_var[i] for i in range(1,11,2)]
for d in range(len(free_var)):
    data_dict['free variables'][list(data_dict['free variables'].keys())[d]] = [float(i.replace(',','')) for i in free_var[d]]


print(data_dict)

# TODO: find the lines byself
# TODO: do this for all files in a directory
# TODO: create a GUI and .exe file from this module
# tpd_res
tpd_res = [i.split() for i in tpd_res]
tpd_res = np.array(tpd_res)[:,0]
tpd_res = [float(i.replace(',','')) for i in tpd_res]
data_dict['tpd results'] = tpd_res


with open('wells data/Well6.json','w') as outfile:
    json.dump(data_dict,outfile)

# read json file again--------------------------


# with open('data_1.json','r') as file:
#     data = json.loads(json.load(file))
# print(data.keys(),type(data))























