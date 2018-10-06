def straight_line(vi, length):
 
    """
    Takes in the initial velocity at the beginning of the current straight road and the current straight road length
    returns the solution of the striahgt road (i.e. velocity vs distance and time taken to reach the road end)
    """    
    
    t = 0          #time elapsed at begining
    s = 0          #distance travelled at the beginning of the road
    list_t = []    #list containing time corresponding to distance travelled list
    list_v = []    #list containing velocity corresponding to distance travelled list
    list_s = []    #list containing distance travelled
    v_max = (rpm[-1]/(FRR*R6*PR))/60*(2*pi)*wheel_raduis   #the max velocity a car can reach on a straight road if the tractive effort is big enough 
    
    while True:
        vf = vi + 0.005   #delta_v = 0.005 found to give accurate solution in this case (it was tuned by decreasing the delta till the change in final solution is minimal)
        v = (vi+vf)/2     #average veocity        
        if v > v_max:     #check that the car doesn't exceed max possible velocity
            v = v_max     #v is the max velocity a car can possibly reach if applicaple 
               
        F = Force_calculator(v) #caculates force.Find it in helper functions
        DF = 0.5*row*(A_aerofoil*Cl_aerofoil_s+A_aerofoil_f*Cl_aerofoil_f)*v**2
        Res = Cr*(9.81*m+DF) + 0.5*row*(Cd*A+Cd_aerofoil_s*A_aerofoil+A_aerofoil_f*Cd_aerofoil_f)*v**2   #resistant force to the car
          #Res has a negative value when v == 0 and that's why I always put intial condition to v, however, initilizing the velocity to 2m/s at beginning doesn't affect the solution by any means so this wasn't optimized further.
            
        if F > meu*(DF+m*9.81):       #car will slip
            F = meu_slip*(DF+m*9.81)  #tracktive force after slipping
                    

        if F <= Res:          #no acceleration so no velocity change
            Res = F           #check that velocity doesn't increaseres when there's no way to increase velocity
            vf = vi           #check that velocity doesn't increaseres when there's no way to increase velocity (no velocity change)
            v = vi
            list_v.append(v)                          #velocity won't increase
            list_s.append((length-s)+list_s[-1])      #add one more element to the list as it now linear relation, i.e, v is constant (the element added is the distance left till the end of the road)
            t = list_t[-1]+(list_s[-1]-list_s[-2])/v  #time taken to finish
            list_t.append(t) 
            return [list_t[-1], v, list_t, list_v, list_s]   #return straight road output for this part of the track 
                                                             #returns >>> time taken, velocity at end, time list, velocity list, distance list and a charachter that shows the road type was (striaght road) 
      
        else:
            list_v.append(v)          #velocity list that represents the velocity of the car on different parts of the track
            a = (F-Res)/m             #acceleration of the car
            t_delta = (vf-vi)/a       #time taken to accelerate from vi to vf
            t += t_delta              #time accumlation
            list_t.append(t)          #time list that corresponds to the velocity and distance lists
            s_delta = v*t_delta       #distance travelled through t_delta
            s += s_delta              #distance accumulation
            list_s.append(s)          #distance list that corresponds to the velocity and time lists
            
        if s >= length: #if striahgt road end reached (when accumulated distance s >= road length) the function will return the following
            return [t, v, list_t, list_v, list_s, 's']      #return straight road output for this part of the track
                                                            #returns >>> time taken, velocity at end, time list, velocity list, distance list and a charachter that shows the road type was (striaght road) 
        else:   
            vi = vf #set new initial velocity equals to the final velocity and the loop keeps going until the straight road end is reached
