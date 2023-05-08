import numpy as np
import pandas as pd
from interpolate_six_files import RGI_WELLs_dict


J = [16.512,16.49,16.49,1.66,1.66,1.663] # STB/d/psi
PR = [238.88,256.11,256.11,209.64,209.64,209.64] # psi

def well_production(GLR,WC,GOR,WHP,J,PR,RGI_well):
    # assuming a Q
    Q=1000
    alpha = 0.01
    while True:
        # Find BHP from tubing table
        BHP_VLP = RGI_well
        # fing BHP from IPR
        BHP_IPR = PR - Q / J
        Q = Q - alpha * (-2/J*(BHP_IPR-BHP_VLP))
        if abs(BHP_IPR-BHP_VLP)<0.00005:
            print('mio',BHP_IPR-BHP_VLP)
            break

    print(Q)

    qw=Q*(1-WC)
    qo=1-qw
    qg=qo*GOR+GLR

    return qo,qg,qw

# TODO: itaration for qo field and ....

df = pd.read_csv('Data_for_Interpolation.csv')

i=0
for row in df.values.tolist():
    Q, GLR, WC, GOR, WHP = row
    qo,qg,qw = well_production(GLR, WC, GOR, WHP,J[0],PR[0],RGI_WELLs_dict['Well1'][i])
    i+=1

