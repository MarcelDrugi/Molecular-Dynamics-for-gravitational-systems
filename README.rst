
| Simple program to modeling many bodies gravitational systems using
| molecular dynamics. The program has gui to visualize the movement of
| celestial bodies and modify simulation parameters in real time.
| 
Newton's equations
~~~~~~~~~~~~~~~~~~
| Motion equations are integrated using two variants of
| Verlet Algorithm (Velocity Verlet and Leapfrog Verlet) and
| two extensions of Euler method (Runge–Kutta fourth-order method
| and Euler-Cromer Method). Own algorithms implementations.
| 
| Three of these algorithms are stable for a fixed time-step that 
| allows model in long time with sufficient performance and a constant 
| error. Runge–Kutta algorithm stability depends on time step size
| what can be demonstrated by using the program
GUI
~~~~~~~~~~~~~~~~~~
| The program contains gui created in PyQt5. GUI allows to visualize 
| of bodies movement and trajectory. It also allows you to modify the 
| time step and choose the algorithm during the simulation.
