#This file defines the class for optimizing
from scipy import optimize as sciopt
from interpolate_unit_convert import interpolation as int
from scipy.optimize import Bounds as bnd 
import numpy as np
import time

#start = time.time()

class optimize:
    def __init__(self):
        self.file = int()
        self.wells_def = {}

    ## Opt 1: Minimize GLR to reach minimum WHP
    def objective(self, x):
        GLrate = x[0]
        return GLrate
    
    def pressure_constraint(self, x, LR, BHP, GOR, WC, pressure_cons_val): #Constraint on minimum 20 bar pressure
        GLR = x[0]
        input_val = (BHP, GOR, WC, GLR, LR) #TNP, GOR, WC and LR are set constant to find optimal GLrate to minimize WHP. Values: 120, 91, 50, GLR, 2000
        interpol = self.file.do_interpolation() #Col 0 = WHP
        res = interpol(input_val)
        cons = res - pressure_cons_val
        return cons
    
    def min_GLR(self, x0, LR, BHP, GOR, WC, pressure_cons_val):
        fun = self.objective
        cons_fun = self.pressure_constraint #Fix this after editing def constraint with more inputs
        bnds = [(0, 119880)] #bounds on GLR = 138 000 old bound
        cons = ({'type': 'ineq', 'fun': cons_fun, 'args': [LR, BHP, GOR, WC, pressure_cons_val]})
        res = sciopt.minimize(fun, x0, method='slsqp', bounds=bnds, constraints=cons) 
        return res
    
    ## Opt 2: max OR, constraint on GLR and min WHP pressure - This is slow because of the optimization needed to find GLR - improved with optimization 3
    def wells(self, wells_WC): # Wells_WC = List of water-cut values
        self.wells_def.clear
        for i in range(len(wells_WC)):
            self.wells_def['WC_well_'+str(i + 1)] = wells_WC[i] 
        return self.wells_def
            
    def obj_OR(self, x, WC_list):
        #WC = self.wells(WC_list)
        LR = x[0]
        OR = LR*(1 - 50/100) #WC['WC_well_'+str(1)]
        return -OR # Negative so we minimize negative oilrate = maximize oilrate
    
    def GL_constraint(self, x, init_guess, WC_list, pressure_cons_val):
        LR = x[0]
        x0 = init_guess
        res = self.min_GLR(x0, LR, 120, 91, 50, pressure_cons_val) #This includes pressure constraint. TODO: MAKE BHP and GOR and WC inputs: WC_list[0]
        GLR = res.x
        return -GLR + 25000
    
    def max_oilrate(self, WC_wells_list, init_guess1opt, pressure_constraint):
        fun = self.obj_OR
        cons_fun = self.GL_constraint 
        bnds = [(750, 3799)] #Bound on the variable, lb = 750 makes sure we dont have two values for same GLR, then it doesnt work. Ub = 3799: highest liquid rate were
            #it's possible to reach 20 bar with "our" GL-rates. Then the GL-rate = 119880.02
        cons = ({'type': 'ineq', 'fun': cons_fun, 'args': [WC_wells_list, init_guess1opt, pressure_constraint]})
        res = sciopt.minimize(fun, [WC_wells_list] ,(1100), method='slsqp', bounds=bnds, constraints=cons) #Feil rekkefølge på args og x0??
        return res
    
    ## Opt 3: minimize deviation with two free variables, one well
    def obj_deviation(self, x, OR_target, GLR_target, w1, w2):
        OR = x[0] #Possible OR
        GLR = x[1] #Possible GLR
        fun = w1*((OR - OR_target)**2) + w2*((GLR - GLR_target)**2)
        return fun
    
    def presscons_deviation(self, x, BHP, GOR, WC, pressure_cons_val): #Constraint on minimum WHP = X bar 
        OR = x[0]
        GLR = x[1]
        LR = OR/(1-(WC/100)) #LR expressed by OR (the free variable)
        input_val = (BHP, GOR, WC, GLR, LR) #TNP, GOR, WC are constants
        interpol = self.file.do_interpolation() #Col 0 = WHP
        res = interpol(input_val)
        cons = res - pressure_cons_val
        return cons
    
    def min_deviation(self, x0, BHP, GOR, WC, presscons_val, OR_target, GLR_target, w1, w2):
        func = self.obj_deviation
        cons_fun = self.presscons_deviation
        lb = [375, 25000]
        ub = [1899, 110000]
        bnds = bnd(lb, ub)
        cons = ({'type': 'ineq', 'fun': cons_fun, 'args': [BHP, GOR, WC, presscons_val]})
        argu = (OR_target, GLR_target, w1, w2)
        res = sciopt.minimize(func, x0, args=argu, method='slsqp', bounds=bnds, constraints=cons)
        return res
    
    ## Opt 4: minimize deviation with two free variables for multiple wells
    def obj_dev_mult(self, x, OR_target, GLR_target, w1, w2, num_wells): #same input as in opt 3, but now these are lists. Maybe OR = x, GLR = y? 
        fun = 0
        for i in range(num_wells):
            res = w1[i]*((x[2*i] - OR_target[i])**2) + w2[i]*((x[2*i + 1] - GLR_target[i])**2)
            fun = fun + res
        return fun
    
    def presscons_dev_mult(self, x, BHP, GOR, WC, pressure_cons_val, counter, num_wells): #same input as in opt 3, but here the input are lists
        LR = x[2*counter]/(1-(WC[counter]/100)) #LR expressed by OR (the free variable)
        GLR = x[2*counter + 1]
        input_val = (BHP[counter], GOR[counter], WC[counter], GLR, LR) #TNP, GOR, WC are constants
        interpol = self.file.do_interpolation() #Col 0 = WHP
        res = interpol(input_val)
        cons = res - pressure_cons_val[0]
        return cons
    
    def glr_tot_cons(self, x, glr_max_limit, num_wells):
        glr_tot = 0
        for i in range(num_wells):
            glr_tot = glr_tot + x[2*i + 1]
        res = glr_max_limit - glr_tot
        return res
    
    def calc_jac(self, x, OR_target, GLR_target, w1, w2, num_wells): #Calculated from the objective function
        jac_list = []
        for i in range(num_wells):
            der1 = 2*w1[i]*(x[2*i] - OR_target[i]) # dfun/dx[i], OR for i = 0, 2, 4, 6, 8
            der2 = 2*w2[i]*(x[2*i+1]-GLR_target[i]) # dfun/dx[j], GLR for j = 1, 3, 5, 7, 9
            jac_list.append(der1)
            jac_list.append(der2)
        return jac_list
    
    def calc_hess(self, x, OR_target, GLR_target, w1, w2, num_wells): #Calculated from the jacobian. Needs x, OR_target, GLR_target as inputs even if they are not used
        hess_arr = np.zeros((2*num_wells, 2*num_wells), int)
        hess_list = []
        for i in range(num_wells):
            der1 = 2*w1[i]
            der2 = 2*w2[i]
            hess_list.append(der1)
            hess_list.append(der2)
        np.fill_diagonal(hess_arr, hess_list)
        return hess_arr
            
    def min_dev_multiplewells(self, algorithm, num_wells, x0, BHP, GOR, WC, presscons_val, glr_max_limit, OR_target, GLR_target, w1, w2, lb, ub):
        func = self.obj_dev_mult
        cons_fun_press = self.presscons_dev_mult
        cons_fun_glr = self.glr_tot_cons
        jacobian = self.calc_jac  
        hessian = self.calc_hess
        bnds = bnd(lb, ub)
        cons1 = {'type': 'ineq', 'fun': cons_fun_glr, 'args': [glr_max_limit, num_wells]} #Constraint on maximum GLR
        cons = [cons1]
        for i in range(num_wells): 
            counter = i
            presscons = {'type': 'ineq', 'fun': cons_fun_press, 'args': [BHP, GOR, WC, presscons_val, counter, num_wells]}
            cons.append(presscons)   
        argu = (OR_target, GLR_target, w1, w2, num_wells)
        res = sciopt.minimize(func, x0, args=argu, method=algorithm, jac='2-point', hess=None, bounds=bnds, constraints=cons) 
        return res
    
## Optimization test 1: Minimize GLR with constraint on pressure
file = optimize() #Do not comment this out when running other optimization problems
file2 = int() #Do not comment this out when running other optimization problems
# x0 = (40000) # x0 for opt: min GLR, x = GLR. x0 = 40 000: 2:27s
# LR = 2000 #Too high LR makes it impossible to reach WHP = 20 bar
# BHP = 120
# GOR = 91
# WC = 50
# minpress = 20
# res = file.min_GLR(x0, LR, BHP, GOR, WC, minpress)
# print(res)
# print(res.x)

# x_val = res.x

# input_val = (BHP, GOR, WC, x_val, LR)
# interpol = file2.do_interpolation(0)
# res2 = interpol(input_val)
# print(f'WHP with GLR = {x_val} is {res2}')

## Optimization test 2: Maximize oil  with GLR constraint - This is slow and improved with optimization 3
    # Opt problem works with:
    # x0 = (0), BHP = 120, GOR = 91, WC = 50, pressure_cons = 20, GL_constraint = 80 000, bounds_lr = (750, 3545). Does not work with GL_constraint 110 000 or higher
    # Ser ut som det er noe som begrenser det til at maks olje er 1570.75, ved 81 942 GLR (når man løsner på begrensningene)
# wells = [50]
# res = file.max_oilrate(wells, x0, 20)
# print(res)
# print(res.fun)
# OR = res.x*(1-(wells[0]/100))
# GLR = file.min_GLR(x0, res.x, BHP, GOR, WC, 20) 
# print(f'The maximum oil rate with the constraint is {OR}, and the gas lift injection is {GLR}')

## Optimization test 3 - minimize deviation for one well

# x0 = [500, 50000] 
# res = file.min_deviation(x0, 120, 91, 50, 20, 1500, 80000, 1, 1)
# print(res)
# print(f'To minimize the objection function, the optimal solution is: Oil rate = {round(res.x[0], 2)} with Gas lift rate = {round(res.x[1], 2)}')

## Optimization test 4 - minimize deviation for multiple wells
# Inputs
# numberofwells = 5 #If this value is less than max possible wells, the result will show the remaining x's equal to x0
# x0 = [500, 30000, 500, 30000, 500, 30000, 500, 30000, 500, 30000]
# BHP = [120, 120, 120, 120, 120]
# GOR = [91, 91, 91, 91, 91]
# WC = [40, 45, 50, 55, 60]
# presscons_val = [20, 20, 20, 20, 20]
# glr_max_limit = 200000
# OR_target = [1600, 1400, 1400, 1400, 1400]
# GLR_target = [35000, 35000, 35000, 35000, 35000]
# w1 = [1, 1, 1, 1, 1] #Weight on OR - OR_target for each well
# w2 = [1, 1, 1, 1, 1] #Weight on GLR - GLR_target for each well
# #lb_var = [600, 15000, 500, 19000, 375, 23000, 300, 25000, 200, 27000] 
# #lb_var = [600, 0, 500, 0, 375, 0, 300, 0, 200, 0] 
# lb_var = [40, 0, 40, 0, 40, 0, 40, 0, 40, 0]
# ub_var = [1899, 110000, 1899, 110000, 1899, 110000, 1899, 110000, 1899, 110000]

# res = file.min_dev_multiplewells('slsqp',numberofwells, x0, BHP, GOR, WC, presscons_val, glr_max_limit, OR_target, GLR_target, w1, w2, lb_var, ub_var)
# print(res)
# for i in range(numberofwells):
#     Totaloil =+ res.x[2*i]    
# print(f'Total oil production is {round(Totaloil, 2)}')

# der = []
# for i in range(numberofwells):
#     result = (res.jac[i*2])/(res.jac[i*2 + 1])
#     der.append(result)
# print(f'The derivative dQoil/dQgaslift for the wells are {der}')

# end = time.time()
# print(f'Execution time is {end - start}')
