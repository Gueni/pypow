import threading
import time
import numpy as np
import matplotlib.pyplot as plt
import ltspice

from matplotlib.animation import FuncAnimation
Vin = 3.3 # V
# Define simulation function
def simulate_boost_converter():
    # Define simulation parameters
    
    Vout = 12.0 # V
    L = 1e-6 # H
    C = 22e-6 # F
    R = 10 # Ohm
    fsw = 100e3 # Hz
    D = (Vout / Vin) / (1 + Vout / Vin) # duty cycle

    # Load the LTSpice simulation file
    lts = ltspice.Ltspice("/home/hunter/Documents/Workspace/Python_code/pypow/boost_converter.asc")
    lts.set_parameters(L=L, C=C, R=R, fsw=fsw, D=D)

    # Run the simulation
    lts.run()

    # Extract simulation results
    t = lts.time
    Vout_sim = lts.get_data("V(out)")
    Iind_sim = lts.get_data("I(L1)")
    Pout_sim = Vout_sim * Iind_sim

    return t, Vout_sim, Iind_sim, Pout_sim

# Define function to update plots
def update_plots(i):
    # Extract simulation results
    t, Vout_sim, Iind_sim, Pout_sim = simulate_boost_converter()

    # Update the time-domain plot
    ax1.clear()
    ax1.plot(t, Vout_sim, label="Vout")
    ax1.plot(t, Iind_sim, label="Iind")
    ax1.plot(t, Pout_sim, label="Pout")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Voltage (V) / Current (A) / Power (W)")
    ax1.legend()

    # Update the switching signal plot
    ax2.clear()
    ax2.plot(t, Vout_sim > (Vin / 2), label="Switching Signal")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Switching Signal")
    ax2.legend()

# Set up the subplots
fig, (ax1, ax2) = plt.subplots(2, 1)

# Set up the animation
ani = FuncAnimation(fig, update_plots, interval=10)

# Run the simulation and animation in separate threads
sim_thread = threading.Thread(target=simulate_boost_converter)
sim_thread.start()

plt.show()
