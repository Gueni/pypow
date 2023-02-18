from time import sleep
import simpy
import matplotlib.pyplot as plt

class BoostConverter:
    def __init__(self, env, input_voltage, output_voltage, inductor_value, capacitance_value, load_value):
        self.env = env
        self.input_voltage = input_voltage
        self.output_voltage = output_voltage
        self.inductor_value = inductor_value
        self.capacitance_value = capacitance_value
        self.load_value = load_value
        
        self.inductor_current = 0
        self.capacitor_voltage = 0
        self.duty_cycle = 0.5
        
        self.time = []
        self.voltage = []
        
        self.action = env.process(self.run())
        
    def run(self):
        while True:
            self.inductor_current += (self.input_voltage * self.duty_cycle - self.output_voltage) / self.inductor_value * self.env.timeout(1e-6)
            self.capacitor_voltage += (self.inductor_current / self.capacitance_value - self.capacitor_voltage / (self.capacitance_value * self.load_value)) * self.env.timeout(1e-6)
            
            self.time.append(self.env.now)
            self.voltage.append(self.capacitor_voltage + self.output_voltage)
            
            yield self.env.timeout(1e-6)
    
    def update_duty_cycle(self, duty_cycle):
        self.duty_cycle = duty_cycle

def plot_voltages(time, voltage):
    plt.plot(time, voltage)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.show()

env = simpy.Environment()
boost_converter = BoostConverter(env, input_voltage=12, output_voltage=24, inductor_value=2e-6, capacitance_value=470e-6, load_value=5)
    
for duty_cycle in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    boost_converter.update_duty_cycle(duty_cycle)
    plot_voltages(boost_converter.time, boost_converter.voltage)
    sleep(1) # add delay to simulate real-time plotting
