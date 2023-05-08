import numpy as np
from interpolate_six_files import interpolate_all_wells

RGI_WELLs_dict = interpolate_all_wells()

J = [7.16,7.151,7.151,0.721,0.721,0.721] # STB/d/psi
PR = [3450,3700,3700,3026,3026,3026] # psi

def well_production(GLR,WC,GOR,WGP,J,PR,RGI_well):
    # assuming a Q
    Q=1000
    # Find BHP from tubing table
    BHP_VLP=RGI_well
    # fing BHP from IPR
    BHP_IPR=PR-Q/J
    # TODO: do itaration

    BHP_VLP-BHP_IPR


    qw=Q*(1-WC)
    qo=1-qw
    qg=qo*GOR+GLR
    return qo,qg,qw

# TODO: itaration for qo field and ....
qo,qg,qw = well_production()
