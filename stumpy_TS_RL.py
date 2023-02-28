import simpy
import numpy as np
import matplotlib.pyplot as plt
import stumpy

# Define circuit parameters
R = 10 # Ohms
C = 1e-3 # Farads
V = 5 # Volts
dt = 1e-5 # Simulation time step

# Define the generator function for the input voltage
def input_voltage(t):
    return V

# Define the RC circuit
def rc_circuit(env,Vin, R, L):
    v = 0  # initial voltage
    i = 0  # initial current
    t = 0  # initial time
    while True:
        # calculate the new voltage and current
        di_dt = (Vin - R * i) / L
        dv_dt = i / C
        i = i + di_dt * dt
        v = v + dv_dt * dt
        t = t + dt
        # yield the voltage value to the simulation environment
        yield v


# Simulate the circuit
env = simpy.Environment()
sim = rc_circuit(env,V, R, C)
results = []
try:
    while True:
        results.append(next(sim))
        if len(results) * dt > 0.1: # Stop the simulation after 0.1 seconds
            break
except StopIteration:
    pass
# print(results)
# Convert the results list to a numpy array with float data type
results = np.array(results).astype(np.float64)

# Perform time series analysis using Stumpy
mp = int(len(results)/10) # Set the m parameter for matrix profile analysis
matrix_profile = stumpy.stump(results, m=mp)

# Plot the simulation results
plt.subplot(2, 1, 1)
plt.plot(np.arange(len(results)) * dt, results)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')

# Plot the matrix profile
plt.subplot(2, 1, 2)
plt.plot(matrix_profile[:, 0], matrix_profile[:, 1])
plt.xlabel('Index')
plt.ylabel('Matrix Profile')
plt.show()
