def straight_line(vi, length, active = False):
 
    """
    returns the solution of the striahgt road (i.e. velocity or vs distance)
    
    """    
    
    active = False #no active wings (active is set to True only when there's active wings installed and performance is to be tested)
    #print(j, active == True)
    

    t = 0 #time elapsed at begining
    s = 0 #distance travelled at the beginning of the road
    list_t = [] #list containing time corresponding to distance travelled list
    list_v = [] #list containing velocity corresponding to distance travelled list
    list_s = [] #list containing distance travelled
    v_max = (rpm[-1]/(FRR*R6*PR))/60*(2*pi)*wheel_raduis #the max velocity a car can reach if the tractive effort is big enough 
    while True:

        vf = vi + 0.005 #delta_v = 0.005 found to give accurate solution in this case (it was tuned by decreasing the delta till the change in final solution is minimal)
        v = (vi+vf)/2 #average veocity        
        if v > v_max: #check that the car doesn't exceed max possible velocity
            v = v_max
               
        F = Force_calculator(v) #caculates force.Find it in helper functions
        DF = 0.5*row*(A_aerofoil*Cl_aerofoil_s+A_aerofoil_f*Cl_aerofoil_f)*v**2
        Res = Cr*(9.81*m+DF) + 0.5*row*(Cd*A+Cd_aerofoil_s*A_aerofoil+A_aerofoil_f*Cd_aerofoil_f)*v**2   #resistant force to the car
          #Res has a negative value when v == 0 and that's why I always put intial condition to v, however initilizing the velocity to 2m/s at beginning doesn't affect the solution by any means so this wasn't optimized further.
            
        if F > meu*(DF+m*9.81): #car will slip
            """ no active wings in the application given with the code so all the lines with the same level of indentation won't be processed """
            if active == True: #if the wing are active check >>> close the wing if found benifical (as both drag and downforce will increase so the better is the one gives more resultant force)
                F_min_drag = F-Res
                max_DF = 0.5*row*(A_aerofoil*Cl_aerofoil_s_S+A_aerofoil_f*Cl_aerofoil_f)*v**2
                max_Res = Cr*(9.81*m+max_DF) + 0.5*row*(Cd*A+Cd_aerofoil_s_S*A_aerofoil+A_aerofoil_f*Cd_aerofoil_f)*v**2
                
                if F > meu*(max_DF+m*9.81):
                    F_max_lift = meu_slip*(max_DF+m*9.81) #max force before slip
                else:
                    F_max_lift = F
                    
                if F_max_lift-max_Res > F_min_drag-Res: #check which gives overall better acceleration and commands the wings to close or stay open
                    F = F_max_lift
                    Res = max_Res
                else:
                    F = F_min_drag
                    #Res = Res 
                    
            else: 
                    F = meu_slip*(DF+m*9.81) #tracktive force after slipping
                    

        if F <= Res: #no acceleration so no velocity change
            Res = F #check that velocity doesn't increaseres when there's no way to increase velocity
            vf = vi #check that velocity doesn't increaseres when there's no way to increase velocity
            v = vi
            list_v.append(v)  #velocity won't increase
            list_s.append((length-s)+list_s[-1]) #add one more element to the list as it now linear relation i.e v is constant (the element added is the distance left till the end of the road)
            t = list_t[-1]+(list_s[-1]-list_s[-2])/v #time taken to finish
            list_t.append(t) 
            return [list_t[-1], v, list_t, list_v, list_s]
        
        else:
            list_v.append(v)
            a = (F-Res)/m             #acceleration of the car
            t_delta = (vf-vi)/a       #time taken to accelerate from vi to vf
            t += t_delta
            list_t.append(t)
            s_delta = v*t_delta
            s += s_delta
            list_s.append(s)
            
        if s >= length: #if striahgt road end reached the function will return the following
            return [t, v, list_t, list_v, list_s, 's'] #time taken, velocity at end, time list, velocity list, distance list and a charachter that corrospons that the road type was striaght road
        else:   
            vi = vf #new initial velocity is the final velocity and the loop keeps going
