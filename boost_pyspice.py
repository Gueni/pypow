import simpy
import plotly.graph_objs as go
from plotly.subplots import make_subplots
# Open the HTML file in the default web browser
import plotly.io as pio
class BoostConverter:
    def __init__(self, env):
        self.env = env
        self.input = simpy.Container(env, init=3.3)
        self.output = simpy.Container(env, init=12)
        self.inductor = simpy.Container(env, init=0)
        self.capacitor = simpy.Container(env, init=0)
        self.switch = False
        self.duty_cycle = 0.5
        self.period = 1/1e3
        self.env.process(self.boost())

    def boost(self):
        while True:
            yield self.env.timeout(self.period)
            self.switch = not self.switch
            if self.switch:
                on_time = self.duty_cycle*self.period
                off_time = (1-self.duty_cycle)*self.period
                yield self.env.timeout(on_time)
                yield self.input.get(1)
                self.inductor.put(1)
                yield self.env.timeout(off_time)
                self.capacitor.put(self.duty_cycle)
                self.inductor.get(1)
            else:
                yield self.env.timeout(self.period*self.duty_cycle)
                yield self.capacitor.get(self.duty_cycle)
                self.output.put(self.duty_cycle*self.input.level/(1-self.duty_cycle))

# Simulation setup
env = simpy.Environment()
boost_converter = BoostConverter(env)

# Data storage
input_data = []
output_data = []
inductor_data = []
capacitor_data = []
power_data = []

# Simulation loop
for i in range(10000):
    env.run(until=(i+1)*1e-6)
    input_data.append((i*1e-6, boost_converter.input.level))
    output_data.append((i*1e-6, boost_converter.output.level))
    inductor_data.append((i*1e-6, boost_converter.inductor.level))
    capacitor_data.append((i*1e-6, boost_converter.capacitor.level))
    power_data.append((i*1e-6, boost_converter.output.level*boost_converter.output.level/12))

fig_list = []
# Generate plots
input_fig = go.Figure()
input_fig.add_trace(go.Scatter(x=[i[0] for i in input_data], y=[i[1] for i in input_data], name="Input Voltage"))
input_fig.update_layout(title="Input Voltage")
fig_list.append(input_fig)

output_fig = go.Figure()
output_fig.add_trace(go.Scatter(x=[i[0] for i in output_data], y=[i[1] for i in output_data], name="Output Voltage"))
output_fig.update_layout(title="Output Voltage")
fig_list.append(output_fig)

inductor_fig = go.Figure()
inductor_fig.add_trace(go.Scatter(x=[i[0] for i in inductor_data], y=[i[1] for i in inductor_data], name="Inductor Current"))
inductor_fig.update_layout(title="Inductor Current")
fig_list.append(inductor_fig)

capacitor_fig = go.Figure()
capacitor_fig.add_trace(go.Scatter(x=[i[0] for i in capacitor_data], y=[i[1] for i in capacitor_data], name="Capacitor Voltage"))
capacitor_fig.update_layout(title="Capacitor Voltage")
fig_list.append(capacitor_fig)

power_fig = go.Figure()
power_fig.add_trace(go.Scatter(x=[i[0] for i in power_data], y=[i[1] for i in power_data], name="Output Power"))
power_fig.update_layout(title="Output Power")
fig_list.append(power_fig)

# Write the figures to an HTML file
with open('figures.html', 'w') as f:
    f.write(pio.to_html(fig_list, full_html=False))



