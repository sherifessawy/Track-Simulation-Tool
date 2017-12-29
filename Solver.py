def simulator(vi, track): #vi is initial velocity, track is a dictionary of form {1:['s', lenght], 2:['c', length, raduis]}

    """
    simulates the track calling the three main functions(straight line, corner, brake) appropriately
    
    """
    i = 0 
    xx = {} #will handle data during solution

    a = straight_line(vi, track[0][1]) #first part of the track is known to be straight line so the straight road function is called
    
    xx[i] = a #a contains t, v, list_t, list_v, list_s of the function called (the solution of the road is added to dic xx)
    i += 1
    s_simulation = [] #distance travelled during the whole simulation
    v_simulation = [] #corresponding velocity
    t_simulation = [] #corresponding time
    
    while i < len(track): #will end itsedlf when track end reached
        if track[i][0] == 'c': # 'c' for corner, so call corner function
            a = corner(xx[i-1][1], track[i][1], track[i][2])
            if len(a) == 1: #it means the function returned on the max velociy of the corner as the car velocity at the entrance was larger than the corner max velocity so it will call the brake function as explained in the corner function
                corrective = brake(xx[i-1][3], xx[i-1][2], xx[i-1][4], a[0]) #solve for new solution(list_v, list_t, list_s, v_max)
                del(xx[i-1]) #deletes old rejected solution of the straight road
                a = corner(a[0], track[i][1], track[i][2]) #call the corner function again but with the accepted entrance velocity; functions arguments (corner(vi, length, raduis))
                xx[i-1] = corrective #new straight road solution
                xx[i] = a #new corner solution
                i += 1
            else:
                xx[i] = a
                i += 1
                

        else:
            a = straight_line(xx[i-1][1], track[i][1]) #call straigh road function; arguments taken (straight_line(vi, length))
            xx[i] = a #add straight road solution to dic xx
            print (round(i/len(track) *100,1), "% of the simulation done") #shows the progress of the solution
            i += 1            
    
    i = 0
    lateral_acc = []
    while i < len(xx):

        if xx[i][-1] == 's':
            lateral_acc += [0]*len(xx[i][3])
        elif xx[i][-1] == 'c':
            for e in xx[i][3]:
                lateral_acc += [(e**2/(xx[i][5]*9.81))]
                
        if i == 0:
            s_simulation += xx[i][4] #as s_list is the 5th element of the dic xx and are added up to form the list-distance of the whole simulation
            v_simulation += xx[i][3] #as v_list is the 4th element of the dic xx and are added up to form the list-velocity of the whole simulation
            t_simulation += xx[i][2] #as t_list is the 3rd element of the dic xx and are added up to form the list-time of the whole simulation
            i += 1
        else:            
            s_simulation_temp = [x+s_simulation[-1] for x in xx[i][4]] #to accumelate distance it adds the last element of the prevoius list to all the elements of the current one
            s_simulation += s_simulation_temp #concatenate the lists (the distances)
            v_simulation += xx[i][3]
            t_simulation_temp = [x+t_simulation[-1] for x in xx[i][2]] # to accumelate time
            t_simulation += t_simulation_temp
            i += 1

    print('lap time', round(t_simulation[-1],3), 'sec')
    print('velocity at end', round(v_simulation[-1],2), 'm/s')   
    #return round(t_simulation[-1],3)
    return [s_simulation, v_simulation,round(t_simulation[-1],3), lateral_acc] #list of the whole track for distance and corresponding velocity and lateral acceleration, also returns time of the lap
