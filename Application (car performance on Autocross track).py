"""
Below is an application to test the performance of the winged car vs non winged car with given specs on given Autocross track of Formula 
Student competition. The Run on an ordinary computer might take up to 5 mins, for both smulations to be conplete.
"""

import numpy as np
import scipy.integrate as integ
from matplotlib import pyplot as plt
from math import pi
import time

""" CAR SPECS """
start_clock = time.clock()
m = 280      #mass kg
A = 0.5738*2       #frontal area m^2
Cd = 0.666807        #coefficint of drag of the car
Cr = 0.014      #coefficint of rolling resistance 
meu = 1.2 #coeff of friction static
meu_slip = 0.8
meu_skid = 0.8
wheel_raduis = 0.254

""" Brake specs """
L = 1.635 #wheel base
L1 = 0.860 #cg location from the front tires
L2 = 0.775 #cg location from the rear tires
h = 0.324 #cg height 

bias_f = 0.6 #bias to front tires
bias_r = 1-bias_f
human_force = 250 #human force on brake pedal
brake_constant = 12.3263
total_brake_force = human_force*brake_constant
Wfs = m*9.81 * L2/L #static weight on the front tires
Wrs = m*9.81 * L1/L #static weight on the rear tires

""" Engine specs """
# Gearing ratios
PR = 2.111   #primary reduction
R1 = 2.666   #1st gear reduction ratio
R2 = 1.937
R3 = 1.611
R4 = 1.409
R5 = 1.260
R6= 1.166
Ri = {'R1':R1,'R2':R2,'R3':R3, 'R4':R4, 'R5':R5, 'R6':R6 }
FRR = 2.7  #Final Reduction ratio

#torque vs rpm

rpm = [0,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,11000,12000,13000,14000,15000]
Engine_torque = [0,15.56, 21.30, 24.61, 30.77, 44.51, 49.17, 52.45, 56.96, 51.66, 47.68, 44.69,40.35,35.37,31.24,28.83]
RPM = 12000 #rpm at which max power occurs
            #at max power rpm = 12000 and is chosen as shifting rpm.

""" aero data """
A_aerofoil = 0.4*0.8  #ref. area of rear wing
A_aerofoil_f = 0.2*0.2*2 #ref. area of front wing

""" front wing"""
Cl_aerofoil_f = 5.7 #cl front wing
Cd_aerofoil_f = 1.0 #cd front wing

""" in our design the rear wing was active, so there were two positions for it. 
One is the max down force position (in corners), and the other is the min drag position (in straight roads). 
However, the kit in this application is static so both have the same value"""

Cd_aerofoil_s_S = 1.109 #cd rear wing during straight roads
Cl_aerofoil_s_S = 5.7059 #cl rear wing during straight roads
Cl_aerofoil_c_S = 5.7059 #cl rear wing during corners
Cd_aerofoil_c_S = 1.1 #cd rear wing during corner

row = 1.2 #density

""" Autocross track """

track = {0: ['s', 7],
  1: ['c', 10, 7.0],
 2: ['s', 15.0],
 3: ['c', 1.0, 5.0],
 4: ['c', 25.0, 27.647],
 5: ['s', 35.0],
 6: ['c', 8.266, 3.9],
 7: ['s', 12.0],
 8: ['c', 7.605, 5.0],
 9: ['s', 80.0],
 10: ['c', 1.0, 5.0],
 11: ['c', 8.2, 5.047],
 12: ['c', 11.582, 6.168],
 13: ['c', 1.0, 5.0],
 14: ['s', 45.0],
 15: ['c', 7.0, 8.0],
 16: ['c', 18.661, 15.215],
 17: ['s', 15.0],
 18: ['c', 1.0, 5.0],
 19: ['s', 85.0],
 20: ['c', 3.5, 5.0],
 21: ['s', 15.0],
 22: ['c', 3.5, 5.0],
 23: ['s', 18.0],
 24: ['c', 9.16, 4.7],
 25: ['s', 10.0],
 26: ['c', 1.0, 5.0],
 27: ['c', 9.263, 6.313],
 28: ['c', 3.0, 5.0],
 29: ['s', 33.0],
 30: ['c', 2.5, 5.0],
 31: ['c', 6.5, 7.324],
 32: ['c', 2.0, 5.0],
 33: ['s', 58.0],
 34: ['c', 3.0, 5.0],
 35: ['c', 26.0, 16.6],
 36: ['c', 35.0, 17.0],
 37: ['c', 25.0, 17.6],
 38: ['c', 15.0, 17.0],
 39: ['s', 28.0],
 40: ['s', 48.0],
 41: ['c', 1.0, 5.0],
 42: ['c', 8.0, 8.6],
 43: ['c', 15.0, 15.0],
 44: ['c', 2.0, 9.0],
 45: ['s', 20.0],
 46: ['c', 10.0, 8.0],
 47: ['c', 10.0, 8.0],
 48: ['c', 5.0, 4.6],
 49: ['s', 50.0],
 50: ['c', 5.0, 5.0],
 51: ['c', 4.0, 3.8],
 52: ['s', 50.0],
 53: ['c', 10.0, 5.0],
 54: ['c', 7.0, 6.0],
 55: ['s', 68.0]} 
 
            
            
""" simulation start """ 
wings = [] #will add solution to it
No_wings = [] #will add solution to it
vi = 2  #initial velocity at the beginning of the track


Cd_aerofoil_s = Cd_aerofoil_s_S #cd for straight road static aerofoil
Cl_aerofoil_s = Cl_aerofoil_s_S #cl during straight road
Cd_aerofoil_c = Cd_aerofoil_s_S #cd during corner
Cl_aerofoil_c = Cl_aerofoil_s_S #cl during corner

j = 1
while j < 3:
    if j == 1:
        print('solution for the car with no wings')
        A_aerofoil=0
        A_aerofoil_f=0    
    if j == 2:
        m += 5 #increased mass of aerokit
        print('solution for car with static wings')
        A_aerofoil_f = 0.2*0.2*2
        A_aerofoil = 0.8*0.4        

     
    a = simulator(vi, track) #solver function
    #print('max lateral acc', round(max(a[-1]),2), 'g')
    
    if j == 2: #wings
        wings.append(a[0]) #a[0] is distance list
        wings.append(a[1]) #a[1] is velocity list
        wings.append(a[-1]) #a[-1] is lateral acceleration list
    if j == 1: #no wings
        No_wings.append(a[0]) #a[0] is distance list
        No_wings.append(a[1]) #a[1] is velocity list
        No_wings.append(a[-1]) #a[-1] is lateral acceleration list
    j += 1

plt.plot(wings[0],wings[1]) #plot distance (m) vs velocity (m/s) for car with wings
plt.plot(No_wings[0],No_wings[1]) #plot distance (m) vs velocity (m/s) for car without wings
