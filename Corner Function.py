def corner(vi, length, raduis):
    
    """
    get the car solution during cornering. calculates also the maximum velocity of a corner. to check if the car is going to skid
    
    """
    t = 0
    s = 0
    list_s = []
    list_v = []
    list_t = []
    meu = 1.2
    v_max = (meu*m*9.81/(m/raduis-0.5*meu*row*(A_aerofoil*(Cl_aerofoil_c_S+A_aerofoil_f*Cl_aerofoil_f))))**0.5 #max velocity through a corner before skidding
    if vi > v_max:
        return [v_max] #it returns v_max if the end velociy of prevoius part of the track is larger than v_max to call and apply brake function
    while True:
        vf = vi + 0.001
        v = (vi+vf)/2
        if v > v_max: #checks that the velocity of the car won't exceed the max velocity through the corner
            v = v_max    
        list_v.append(v)
        F = Force_calculator(v)
        DF = 0.5*row*(A_aerofoil*Cl_aerofoil_c_S + A_aerofoil_f*Cl_aerofoil_f)*v**2
        if F > meu*(DF+m*9.81):
            F = meu*(DF+m*9.81)
        Res = Cr*(9.81*m+DF) + 0.5*row*(Cd*A+Cd_aerofoil_c_S*A_aerofoil+A_aerofoil_f*Cd_aerofoil_f)*v**2   #resistant force to the car
       
        a = (F-Res)/m             #acceleration of the car
        #print(a)
        t_delta = (vf-vi)/a           #time taken to accelerate from vi to vf
        t += t_delta
        list_t.append(t)
        s_delta = v*t_delta
        s += s_delta
        list_s.append(s)
        if s >= length: #end function if distance travelled is biggere than corneer length
            #plot(list_s, list_v)
            return [t, v, list_t, list_v, list_s, raduis, 'c']
        else:   
            vi = vf
