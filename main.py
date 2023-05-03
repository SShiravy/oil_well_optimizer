import time
from optimizer import optimize

start = time.time()
## Run optimizer from this script
# Define object
opt_case1 = optimize()
# Input to optimizer
numberofwells = 5 #If this value is less than max possible wells, the result will show the remaining x's equal to x0
x0 = [500, 30000, 500, 30000, 500, 30000, 500, 30000, 500, 30000]#, 500, 30000, 500, 30000, 500, 30000] # oil,gas ...
BHP = [120,120, 120, 120, 120]#, 120, 120, 120]
GOR = [91, 91, 91, 91, 91]#, 91, 91, 91]
WC = [40, 45, 50, 55, 60]#, 57, 57, 59]
presscons_val = [20, 20, 20, 20, 20]#, 20, 20, 20]
glr_max_limit = 200000
OR_target = [1600, 1400, 1400, 1400, 1400]#, 1400, 1400, 1400]
GLR_target = [35000, 35000, 35000, 35000, 35000]#, 35000, 35000, 35000]
w1 = [50, 1, 1, 1, 1]#, 1, 1, 1] #Weight on OR - OR_target for each well
w2 = [1, 1, 1, 1, 1]#, 1, 1, 1] #Weight on GLR - GLR_target for each wel
lb_var = [40, 0, 40, 0, 40, 0, 40, 0, 40, 0]#, 40, 0, 40, 0, 40, 0]
ub_var = [1899, 110000, 1899, 110000, 1899, 110000, 1899, 110000, 1899, 110000]#, 1899, 110000, 1899, 110000, 1899, 110000]

# Run optimization
res = opt_case1.min_dev_multiplewells('slsqp',numberofwells, x0, BHP, GOR, WC, presscons_val, glr_max_limit, OR_target, GLR_target, w1, w2, lb_var, ub_var)
print('result:',res)

# Print extra information of the result
Totaloil = 0
der = []
TotalGL = 0
for i in range(numberofwells):
    ## Find total oil
    Totaloil = Totaloil + res.x[2 * i]
    ## Find Jacobian dQoil/dQgaslift
    der.append((res.jac[i * 2 + 1]) / (res.jac[i * 2]))
    ## Print total gas lift injection used:
    TotalGL = TotalGL + res.x[2 * i + 1]
print(f'Total oil production is {round(Totaloil, 2)}')
print(f'The derivative dQoil/dQgaslift for the wells are {der}')
print(f'Total gas lift injection used is {round(TotalGL, 2)}')

end = time.time()
print(f'Execution time is {end - start}')

# TODO: do this for all data files in a directory
