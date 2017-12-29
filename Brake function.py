def brake(list_v, list_t, list_s, v_max): #calculate required braking distance and the crossponding velocity change per time
    a = 0 #deceleration initilaization

    """
    it takes in the cumlitive velocity with distance and calculates the braking distance 
    
    it iterates using bisecion search alogarith to reach the braking distance    
    
    """
    list_v_temp = list_v[:]
    list_t_temp = list_t[:]
    list_s_temp = list_s[:]
    correction_index = 0 #to evaluate/get final lists
    while True:      
        s_rest = list_s[-1]-list_s[len(list_v)//2]
        s_current = list_s[len(list_v)//2]
        #print('s_rest',s_rest)
        vi = list_v[len(list_v)//2 - 1]
        #print('vi', vi)
        t_current = list_t[len(list_t)//2]
        #print('t_current', t_current)
  
        
        t = 0
        t_delta = 0 #used for break function calculation in 4dof system (time step)
        w0=[0,0,0,0,0,0,0,0] #used for brake function calculation in 4-dof system (initial conditions)
        ############
        
        s = 0 #distance travelled at beginning of braking is zero for each trial. this will still be added and fitted in the global solution
        c = 0 #counter
        #print (1)
        list_v_brakes = [] #to capture new v with crossponding distance  #new list that will be used for updating the global solution if the trial was accepted
        list_t_brakes = [] #to capture new t with crossponding distance  #new list that will be used for updating the global solution if the trial was accepted
        list_s_brakes = [] #to capture new s basing on the new velocity on the track #new list that will be used for updating the global solution if the trial was accepted
        while True:
            c += 1

            """
            tuned velocity difference (dv), to avoid any simulation inaccuracy, was set to 0.005. 
            You can change it to make sure it fits your model. for example, in this case, dv of 0.01 found to give accurate solution
            """
            vf = vi - 0.005  
            v = (vi+vf)/2
            list_v_brakes.append(v)
            #print(v)
            if v < v_max*0.95:
                break
            DF = 0.5*row*(A_aerofoil*Cl_aerofoil_c_S+A_aerofoil_f*Cl_aerofoil_f)*v**2 #wings Down force total
            DFF = 0.5*row*(A_aerofoil_f*Cl_aerofoil_f)*v**2 #wings Down force front
            DFR = 0.5*row*(A_aerofoil*Cl_aerofoil_c_S)*v**2 #wings Down force rear 
            sol = calc_brake(a, DF,DFF, DFR, v, t_delta, w0)
            Res = sol[0] #resistance on car
            w0 = sol[1] #new initial condition to be fed back in the next time step. It will be fed back t the function calc_brake
            a = -Res/m #deceleration rate

            t_delta = -(vi-vf)/a #time taken to decelerate from vi to vf
            #print (t_delta)
            t += t_delta #time accumulation
            list_t_brakes.append(t+ t_current)
            s_delta = v*t_delta #distance travelled during the time calculated
            s += s_delta #distance accumulation
            #print(s, s_rest)
            list_s_brakes.append(s+ s_current) #new list that will be used for updating the global solution if the trial was accepted
            #print ('solve for new v distance', s)
            if s >= s_rest:

                if v_max >= v >= v_max*0.98: #limits where the vl will be accepted 
                    list_v_overall = list_v_temp[0:correction_index] + list_v_brakes #to get a list of the new v on the given straight line or corner
                    list_t_overall = list_t_temp[0:correction_index] + list_t_brakes #to get a list of the new t on the given straight line or corner
                    list_s_overall = list_s_temp[0:correction_index] + list_s_brakes
                    t = list_t_overall[-1]                    
                    
                    return t, v, list_t_overall, list_v_overall, list_s_overall, 's'
                else:
                    break
            else:
                vi = vf
        if v < v_max: #bisection search method
            correction_index += len(list_v)//2
            list_s = list_s[len(list_v)//2:]
            list_v = list_v[len(list_v)//2:]
            list_t = list_t[len(list_t)//2:]
        elif v > v_max: #bisection search method
            list_s = list_s
            list_v = list_v[0:len(list_v)//2]
            list_t = list_t[0:len(list_t)//2]
            
            
