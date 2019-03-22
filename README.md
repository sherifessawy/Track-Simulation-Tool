# Track-Simulation-Tool
The code provided is tested for limited cases simulating the performance of Formula Student race car on different tracks. It was a part of a project done by [ASU Racing Team](http://asuracingteam.org/) participating in [FSUK](https://www.imeche.org/events/formula-student) competition. The code formulation will be briefly discussed, and a guide will be provided, if there's an interest to use the code for your own simulation.

This [paper](https://www.sae.org/publications/technical-papers/content/2019-01-1128/), presented at WCX SAE World Congress Experience, explains the code formulation, car modeling on track and analysis done using the code.

## Scope
The scope of this project was to test multiple designs for the aerodynamic kit, to be installed on ASURT Formula Student car, on Autocross track of the competition. The code was slightly improved, as will be explained later, to optimize the brake design along with the installed aerodynamic kit.

## Assumptions 
A compromise between computational complexity and solution accuracy is done leading to the following assumptions:
1. Shifting time is zero (in case of ICE car)
2. No transmission losses. (However, it can be considered while providing the Torque vs RPM curve of the engine or the motor)
3. Transition from acceleration to braking is instantaneous. 

## Code weaknesses
guided by the scope of the project and modeling simplicity, the following simplifications has been made:
1. The tire model used while making this code was a simple one that sometimes it leads to nonrealistic behaviours (i.e, while braking). 
   1. This behavior was partially overcome by accounting for the transient response of the car while weight transfer is being calculated, simulating the car as 4-degrees of freedom while braking.
2. The code simulates the car as a point mass while cornering, but it also maintains the maximum velocity of the car while cornering at acceptable limits. So that it won't lead to not realistic results due to simple modeling (i.e. the speed of the car is controlled so that no skidding or rolling will occur while cornering)

## Systems modeling 
The car systems that are modeled and that will be asked as inputs, besides the track, are:
1. Aerodynamic kit (e.g, Cd, Cl of the wings). 
**If no kit installed**, its area is set to Zero
2. Brake system (e.g, bias ratio, brake constant, C.G location)
3. Car different parameters (e.g, Engine torque vs. rpm, car sprung/unsprung masses, spring stiffness, etc.)

For simplicity, the car is modeled as point mass during acceleration. But it is modeled as 4-degrees of freedom, or "bicycle" model (shown in Figure 2) during braking. The reason for that will be explained in **performance gap** section.

### Modeling during braking
Lateral or longitudinal weight transfer, is the amount of change on the vertical loads of the tyres due to the longitudinal acceleration imposed on the centre of gravity (CG) of the car. In other words, it is the amount Weight transfer by which vertical load is increased on the front tyres and reduced from the rear tyres when the car is decelerating.
 
#### Point mass modeling during braking
The total weight transfer on the car can be calculated from its free body diagram, as shown in figure 1. In the image, the car is looked from the rear in a right hand turn. Here, Ay is the lateral acceleration in G units, is the W weight of the car, h is the CG height, t is the track width and FyL and FyR are the vertical loads on the left and right tyres, respectively. In a similar fashion, longitudinal weight transfer can be calculated.

![capture](https://user-images.githubusercontent.com/27374894/46210505-2ff1f500-c331-11e8-9503-81139d68f11f.PNG)

**Figure 1. lateral weight transfer of a vehichle**  

#### Four-degrees of freedom modeling during braking

Four more equations were added to account for the transient response of the car to reach the final condition

![20562638_10213236318492003_839197412_n](https://user-images.githubusercontent.com/27374894/46210573-5f086680-c331-11e8-9b81-287a8748ce62.png)

**Figure 2. 4-degrees of freedom model** 

### Performance gap of the two models during braking

![figure_1-3](https://user-images.githubusercontent.com/27374894/46210603-72b3cd00-c331-11e8-8162-64771587c97f.png)

**Figure 3. Performance gap between point mass and 4 degrees of freedom model** 

The point mass model exhibits discontinuity in the deceleration rate as seen in Figure 3 due to simplistic tire model and due to that the equations of point mass model, unlike the 4-DOF model, don't take into consideration the time taken to reach the final position after the weight transfer has taken place. It only calculates the final positions based on discrete inputs (as seen in equations in Figure 1). 

**The not realistic behavior was due to simple tire model:** while braking there was a discontinuous change in deceleration rate as the output and the inputs for the equations in Figure 1 was dependent. As shown in Figure 4, decelration affects the weight transfer that affects the wheel loads that affects the tyres skid ratio which in turns affects the deceleration. And since the tyre model used here has one of two values (the car tyre is either skidding or not) this not realistic behavior appeared.

![image](https://user-images.githubusercontent.com/27374894/46214873-51a4a980-c33c-11e8-9ff7-034fb65143d0.png)

**Figure 4, dependent variables**

Since the equations in figure 1 did not take into consideration the time taken by the car to reach the final steady state condition after the weigh transfer has taken place. To overcome this behavior, 4 more equations were added to account for the transient response of the car to reach the final condition, This partially solved the issue  as seen in Figure 3.

**This behaviour should be overcome completely when the tyre model used is one that resembles the real case and not a simplistic one**

## Code Formulation
The code consists of 4 main functions:
1. Straight road (simulates and outputs the sol. of the car on straight road - acceleration only)
2. Corner (simulates and outputs the sol. of the car on corners acceleration only, with the max velocity through a corner condition)
3. Brake (simulates and outputs the sol. of the car on straight road and corners deceleration)
4. Solver (connects the 3 functions to output the overall solution)

## Code performance
The code provided in this Repo solves each part of the track disregarding solution potential similarities over some parts of the track. This made the code much slower to finish a simulation due to iterative functions and functions that include integration processes, shown in equations in Figure 1. Another approach was presented that made the code 10 times faster.

**What is the other approach?**
The other approach which is provided only through the Jupyter notebook file (which is a complete simulation for the car on Autocross track), is to calculate the universal solution for the car decelerating from max velocity to zero. This solution is the used to update the solution throughout the track without actually having to calculate it again. For instance, if the car is braking from velocity = 50 km/hr to velocity = 20 km/hr, it will directly extract this part of the universal solution without having to calculate it again.

## A guide to use the code
1. Download the excel file (Car specs) and add all the required inputs (some of the inputs are optional and all explained in the excel sheet)
2. Use the Juypyter notebook provided (Track simulation) to run the code and provide the path to the excel file in the second cell or upload it without changing its name.
3. Run all cells and the results will be saved to a csv file

* Note that the jupyter notebook provided is the only version that is adjusted to extract the values from the excel sheet

## Optional
While giving in input to the excel sheet 2 things are optional:
1. In case of simulating performance of car with wings, you can choose either to make the wings active or static. Static wings will keep Cd and Cl constant on any part of the track. However, the active wings option, will take extra inputs which is the minimum drag position values of Cd and Cl of the wing, and will be used only in straight roads to maximize car acceleration.
2. You can choose whether or not to run the 4-DOF model which will require extra inputs if you want to run it.

## system optimization technique 
To make a decision about the design. Brute force method was used, simulating selected combinations of bias ratio for the brake system vs different designs of the aerodynamic kit with corresponding Lift and Drag coefficients. The combination that gave the minimum lap time, Hence more points in the competition was selected.
