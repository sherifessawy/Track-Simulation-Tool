def interpolater(Rpm, rpm, Engine_torque):
    """
    interpolates for the car toruqe vs rpm curve
    
    """    
    i = 1
    while i < len(rpm):
        if rpm[i-1] <= Rpm <= rpm[i]:
            break
        else:
            i += 1
    torque = ((Rpm-rpm[i-1])/(rpm[i]-rpm[i-1]))*(Engine_torque[i]-Engine_torque[i-1])+Engine_torque[i-1]
    return torque


def Force_calculator(v):
    
    """
    calculates wheel forces (tractive effort)
    
    """
    if 0 <= v < (RPM*2*pi/60)/(PR*FRR*R1)*wheel_raduis:
        R = Ri['R1']
        #print('R1')
    elif (RPM*2*pi/60)/(PR*FRR*R1)*wheel_raduis <= v < (RPM*2*pi/60)/(PR*FRR*R2)*wheel_raduis:
        R = Ri['R2']
        #print('R2')
    elif (RPM*2*pi/60)/(PR*FRR*R2)*wheel_raduis <= v < (RPM*2*pi/60)/(PR*FRR*R3)*wheel_raduis:
        R = Ri['R3']
        #print('R3')
    elif (RPM*2*pi/60)/(PR*FRR*R3)*wheel_raduis <= v < (RPM*2*pi/60)/(PR*FRR*R4)*wheel_raduis:
        R = Ri['R4']
        #print('R4')
    elif (RPM*2*pi/60)/(PR*FRR*R4)*wheel_raduis <= v < (RPM*2*pi/60)/(PR*FRR*R5)*wheel_raduis:
        R = Ri['R5']
    else:
        R = Ri['R6']
    F = wheel_torque(v,R)/wheel_raduis
    #print(F)
    return F

#Torque calculation 

def wheel_torque(v,R): #returns wheel toruqe

    rpm_wheel = (v/wheel_raduis)*(60/(2*pi)) 
    rpm_engine = rpm_wheel*FRR*R*PR
    #print('rpm_engine', rpm_engine)
   
    torque = interpolater(rpm_engine, rpm, Engine_torque) #interpolates for the car toruqe vs rpm curve
    wheel_torque = torque*FRR*PR*R
    return  wheel_torque   
