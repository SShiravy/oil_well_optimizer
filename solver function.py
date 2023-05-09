import numpy as np
import pandas as pd
from interpolate_six_files import RGI_WELLs_dict

J = [16.512,16.49,16.49,1.66,1.66,1.663] # STB/d/psi
PR = [238.88,256.11,256.11,209.64,209.64,209.64] # psi

def well_production(GLR,WC,GOR,WHP,J,PR,RGI_well):
    # assuming a Q
    Q= 100
    alpha = 0.1
    while True:
        # Find BHP from tubing table
        BHP_VLP = RGI_well
        # fing BHP from IPR
        BHP_IPR = PR - Q / J

        # Q -= 0.1 * (BHP_VLP-BHP_IPR)
        Q = Q - alpha * (-2/J*(BHP_IPR-BHP_VLP)) # Gradient Decent : Q - d/dQ f(Q) ; f(Q)= BHP_BLP - PR - Q/J
        if abs(BHP_IPR-BHP_VLP)< 1e-6:
            print('BHP_IPR-BHP_VLP:',BHP_IPR-BHP_VLP)
            print('Q:', Q)
            break

    qw=Q*(1-WC)
    qo=1-qw
    qg=qo*GOR+GLR

    return qo,qg,qw


df = pd.read_csv('Data_for_Interpolation.csv')

for num_well in range(6): # 6 for six json file
    print(f'well number {num_well+1}---------------------------------')
    RGI_well_list = list(RGI_WELLs_dict.values())[num_well]
    for num_row in range(len(df.index)):
        print(f'row number {num_row}')
        Q, GLR, WC, GOR, WHP = df.values.tolist()[num_row]
        RGI_well = RGI_well_list[num_row]
        qo,qg,qw = well_production(GLR, WC, GOR, WHP,J[num_well],PR[num_well],RGI_well)

