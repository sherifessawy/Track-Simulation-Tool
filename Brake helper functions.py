""" below are functions called in brake function """            
            
            
def vib(w0,t,p):

    f = integ.odeint(four_dof_msd, w0, t, args=(p,)) #vibrational analysis for the system
    return f

weight_rear = []
weight_front = []

###############################################################################################################################

def weight_transfer(a, dt, w0, DFF, DFR):
    """ calculates weight transfer, w0 is the initial condition and is updated with each time step by feeding back the output of the prevouis time step  """
   
    Wt = m* (-a) * h/L
    f_f =  Wt + DFF #weight transfer front + down force front
    f_r =  -Wt + DFR
    
    #return Wt+Wfs, -Wt+Wrs, 1 #if not hashed the vibrational analysisn won't take place and the model will be point mass
    
    t=np.linspace(0,dt,2) 
    p = [L1,L2,62.3876,280,20*2,80000*2,250000*2,5560*2, f_f, f_r]
    soln = vib(w0,t,p)
    
    Wr = -soln[-1,6]*250000*2 #units N
    Wf = -soln[-1,4]*250000*2
    
    return Wf+Wfs, Wr+Wrs, soln[-1,:] #soln[-1,:] is the new initial condition at the next time step
        
    ##################################################################################################################

def calc_brake(a, DF,DFF,DFR, v, dt, w0):
    """ calculates brake force based on a given bias ratio, w0 is the boundary conditions """
    
    Res_aerodynamic = 0.5*row*(Cd*A+A_aerofoil_f*Cd_aerofoil_f+Cd_aerofoil_c_S*A_aerofoil)*v**2 
    a_aerodynamic = - Res_aerodynamic/m #deceleration dure to aerodynamic forces
    #print(DFF,DFR)
    #print(a,v)
    w_f, w_r, w0 = weight_transfer(a - a_aerodynamic, dt, w0, DFF, DFR) # a-a_aerodynamic as the aerodynamic resistance act againist weight transfer
    
    if total_brake_force*bias_f < w_f*meu:
        Res_f = total_brake_force*bias_f
    else:
#        print('slip fr', v, )
        Res_f = w_f*meu_slip
        
    if total_brake_force*bias_r < w_r*meu:
        #print (v,(DFR+w_r)*meu)
        Res_r = total_brake_force*bias_r
    else:
#        print('slip rear', v, (DFR+w_r)*meu)
        Res_r = w_r*meu_slip  
        
    Rolling_Res = Cr*(9.81*m+DF)
    
    return Res_f + Res_r + Res_aerodynamic + Rolling_Res, w0 #w0 will be keep carried back as it will be used as the inpput in the next time step initial condition (this can be sidetracked if w0 can be defined as a global variable)

#######################################################################################################################

def four_dof_msd(s,t,p):
    
    theta,omega,x,y,x1,y1,x2,y2=s #initial conditions
    a1,a2,Is,ms,mus,k,kt,c, f1, f2=p #Cg location(a1,a2), moment of inetria, mass sprung, mass unsprung, stiffness, damping coeff
    
    yy1 = 0
    yy2 = 0
    
    smass_acc = (c*(y-y1-a1*omega) + c*(y-y2+a2*omega)\
                + k*(x-x1-a1*theta) + k*(x-x2+a2*theta) + f1 + f2)/-ms
    smass_ang_acc = (-a1*c*(y-y1-a1*omega) + a2*c*(y-y2+a2*omega)\
                - a1*k*(x-x1-a1*theta) + a2*k*(x-x2+a2*theta) - f1*a1 + f2*a2)/-Is                
    usmass_accf = (-c*(y-y1-a1*omega) + kt*(x1-yy1) - k*(x-x1-a1*theta))/-mus
    usmass_accr = (-c*(y-y2+a2*omega) + kt*(x2-yy2) - k*(x-x2+a2*theta))/-mus
    
    f=np.array([omega,
                smass_ang_acc,
                y,
                smass_acc,
                y1,
                usmass_accf,
                y2,
                usmass_accr])
    
    return f
