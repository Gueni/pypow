import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from multiprocessing import Process, Queue
import time

# Capacitance and resistance values
C = 1e-6  # Capacitance in Farads
R = 10e3  # Resistance in Ohms

# Simulation parameters
t0 = 0  # Initial time
tf = 1  # Final time
dt = 1e-2  # Time step
n = int((tf - t0) / dt) + 1  # Number of time steps

# Initial conditions
V0 = 0.5  # Initial voltage across capacitor
I0 = 0.5  # Initial current through resistor
x0 = np.array([V0, I0])  # Initial state vector
c=0
# Define the derivative function
def f(x):
   
    V, I = x  # State variables
    dV = I / C  # Rate of change of voltage
    dI = -V / R / C  # Rate of change of current
    print(f"{c+1},V={V:.3f}, I={I:.3f}\n")
    return np.array([dV, dI])  # Return derivative vector

# Calculate the Jacobian matrix
Jf = np.array([[0, 1/C], [-1/(R*C), 0]])

# Set up the figure and axes for the plot
fig, ax = plt.subplots()
ax.set_xlim(t0, tf)
ax.set_ylim(-0.1, V0 + 0.1)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Voltage (V)')

# Initialize the plot elements
line, = ax.plot([], [])
text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

# Define the function to calculate the simulation
def calculate(q):
    x = x0
    q.put(x)
    for i in range(1, n):
        x = x + dt * f(x)
        q.put(x)

# Define the animation function
def animate(i):
    if not q.empty():
        x = q.get()
        x_plot[i] = x
        line.set_data(np.linspace(t0, t0 + i * dt, i + 1), x_plot[:i + 1, 0])
        text.set_text(f'Time = {t0 + i * dt:.4f} s')
    return line, text

# Set up the plot
x_plot = np.zeros((n, 2))
x_plot[0] = x0

if __name__ == "__main__":
    # Set up the queue and process for the simulation
    q = Queue()
    p = Process(target=calculate, args=(q,))
    p.start()

    # Set up the animation
    ani = FuncAnimation(fig, animate, frames=n-1, blit=True)

    # Start the simulation and animation
    plt.show()

    # Join the simulation process
    p.join()
