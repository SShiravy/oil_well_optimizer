import numpy as np
from interpolate_six_files import interpolate_all_wells

RGI_WELLs_dict = interpolate_all_wells()

def well_production(GLR,WC,GOR,WGP,J,PR,RGI_well):
    # assuming a
    Q=1000
    # Find BHP from tubing table
    BHP_VLP=RGI_well
    # fing BHP from IPR
    BHP_IPR=PR-Q/J
    # TODO: do itaration
    qw=Q*(1-WC)
    qo=1-qw
    qg=qo*GOR+GLR
    return qo,qg,qw


# TODO: itaration for qo field and ....
qo,qg,qw = well_production()
