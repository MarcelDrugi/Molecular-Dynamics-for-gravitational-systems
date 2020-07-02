# <span style="color:red"> Running the application </span>
#### To start the app, follow the steps below.
###### 1. Clone repo:
    git clone https://github.com/MarcelDrugi/Molecular-Dynamics-for-gravitational-systems
###### 2. Go to app directory:
     cd Molecular-Dynamics-for-gravitational-systems/
###### 3. Create virtual environment:
    virtualenv venv 
###### 4. Activate venv:
    source venv/bin/activate
###### 5. Install requirements:
    pip3 install -r  requirements.txt
###### 6. Run app:
    python3 __main__.py 


## 
# App description

Simple program to modeling many bodies gravitational systems using<br>
molecular dynamics. The program has gui to visualize the movement of<br>
celestial bodies and modify simulation parameters in real time.
 
### Newton's equations

Motion equations are integrated using two variants of<br>
Verlet Algorithm (Velocity Verlet and Leapfrog Verlet) and<br>
two extensions of Euler method (Runge–Kutta fourth-order method<br>
and Euler-Cromer Method). Own algorithms implementations.<br>
<br>
Three of these algorithms are stable for a fixed time-step that <br>
allows model in long time with sufficient performance and a constant <br>
error. Runge–Kutta algorithm stability depends on time step size<br>
what can be demonstrated by using the program

### GUI
The program contains gui created in PyQt5. GUI allows to visualize <br>
of bodies movement and trajectory. It also allows you to modify the <br>
time step and choose the algorithm during the simulation.

