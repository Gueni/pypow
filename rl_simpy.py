from matplotlib.animation import FuncAnimation
import simpy
import matplotlib.pyplot as plt
import numpy as np

# define the RL circuit simulation function
def rl_circuit(env, output, timestep):
    current = 0.0
    voltage = 0.0
    while True:
        # simulate the resistance and inductance
        voltage = output[-1] if len(output) > 0 else 0.0
        self_inductance = current * env.timestep / env.L
        self_resistance = current * env.R
        current += ((env.input_voltage - voltage) / env.L - self_resistance - self_inductance) * timestep
        output.append(current * env.R)
        yield env.timeout(timestep)

# define the GUI class
class RL_GUI:
    def __init__(self, sim_env):
        self.sim_env = sim_env
        self.current = []
        self.voltage = []
        self.time = []

        # set up the plot
        self.fig, self.ax = plt.subplots()
        self.current_line, = self.ax.plot(self.time, self.current, label="Current")
        self.voltage_line, = self.ax.plot(self.time, self.voltage, label="Voltage")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Current (A) / Voltage (V)")
        self.ax.legend()

    def update_plot(self, current):
        self.current.append(current)
        self.voltage.append(self.sim_env.output[-1] if len(self.sim_env.output) > 0 else 0.0)
        self.time.append(self.time[-1] + self.sim_env.timestep if len(self.time) > 0 else 0.0)
        self.current_line.set_data(self.time, self.current)
        self.voltage_line.set_data(self.time, self.voltage)
        self.ax.relim()
        self.ax.autoscale_view()

    def animate(self):
        ani = FuncAnimation(self.fig, self.update_plot, interval=10, blit=False)
        plt.show()

# create the simulation environment and GUI
sim_env = simpy.Environment()
sim_env.timestep = 0.1
sim_env.L = 10e-3
sim_env.R = 1e3
t = np.arange(0, 1, sim_env.timestep)
sim_env.input_voltage = 55
sim_env.output = []


gui = RL_GUI(sim_env)

# start the simulation and animation
sim_env.process(rl_circuit(sim_env, sim_env.output, sim_env.timestep))
gui.animate()
