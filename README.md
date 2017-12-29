# Track-Simulation-Tool
The code provided is tested for many, but not all, cases simulating the performance of Formula Student race car with on different tracks. It was a part of a project done by [ASU Racing Team](http://asuracingteam.org/) participating in [FSUK](https://www.imeche.org/events/formula-student) '17. The code formulation will be briefly discussed, and a guide will be provided, if there's an interest to use the code for your own simulation.

## Assumptions 
A comprmise between computational complexity and solution accuracy is done leading to the following assumptions:
1. Shifting time is zero (in case of ICE car)
2. No transimission losses. (However, it can be considered while providing the Torque vs RPM curve of the engine or the motor)
3. Transition from acceleration to braking is instantenoues. 

## Systems modeling 
The car systems that are modeled, beside the track, and that will be asked as input for the code are:
1. Aerodynamic kit (e.g, Cd, Cl of the wings)
2. Brake system (e.g, bias ratio, C.G location)
3. Car different parameters (e.g, car sprung/unsprung masses, spring stiffness, etc.)

The car is modeled as point mass during acceleration, and is modeled as 4-degrees of freedom, or "bicycle" model (shown in Figure 1) during braking. The reason for that is shown in Figure 2. The results showed difference in solution and unphysical behaviors of the point mass model during braking.
![20562638_10213236318492003_839197412_n](https://user-images.githubusercontent.com/27374894/34449280-58e2bd72-ecff-11e7-8a38-c0c2bafb8b99.png)

**Figure 1. 4-degrees of freedom model** 
![h](https://user-images.githubusercontent.com/27374894/34449222-c4feb692-ecfe-11e7-86e5-0e2eb2d09f72.png)

**Figure 2. Performance gap between point mass and 4 degrees of freedom model** 

## Code Formulation
The code consists of 4 main functions:
1. Straight road (function that solves the car on straight road acceleration only)
2. Corner (function that solves the car on corners acceleration only, with the max velocity through a corner condition)
3. Brake (function that solves the car on straight road and corners deceleration)
4. Solver (function that connects the 3 functions to output the overall solution)

## Code performance
The code provided in this Repo solves each part of the track disregarding the solution history. However, this was found to be slow to finish a simulation due to iterative functions, and functions that ininclude lots of integeration processes, shown in equations in Figure 1. Although it's more accurate to solve for the car performance on track this way, since that the transient response of the 4-degrees of freedom model slightly differs depending on the tarting velocity, another approach was presented that made the code 10 times faster.

**What is the other approach?**
The other approach which is provided through the Jupyter notebook file, is to calculate the universal solution for the car accelerating from zero to maximum velocity, and decelerating from max velocity to zero. This solution is the used to update the solution throughout the track without actually having to calculate it again. For instance, if the car is braking from velocity = 50 km/hr to velocity = 20 km/hr, it will directly extract this part of the universal solution without having to calculate it again.

## A guide to use the code
1. Download the excel file and add all the required inputs (some of the inputs are optional and all explained in the excel sheet)
2. Use the Juypyter notebook provided to run the code and provide the path to the excel file in the second cell or upload it without changing its name.
3. Run all cells and the results will be saved to a csv file
