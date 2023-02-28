import simpy
import matplotlib.pyplot as plt

class PWMGenerator:
    def __init__(self, env, duty_cycle, period):
        self.env = env
        self.duty_cycle = duty_cycle
        self.period = period
        self.output = None
        self.output_history = []
        self.time_history = []
        self.process = env.process(self.run())

    def run(self):
        while True:
            self.output = 1
            self.output_history.append(self.output)
            self.time_history.append(self.env.now)
            yield self.env.timeout(self.duty_cycle * self.period)
            self.output = 0
            self.output_history.append(self.output)
            self.time_history.append(self.env.now)
            yield self.env.timeout((1 - self.duty_cycle) * self.period)

env = simpy.Environment()
pwm = PWMGenerator(env, duty_cycle=0.5, period=1)
env.run(until=10)

plt.plot(pwm.time_history, pwm.output_history)
plt.xlabel('Time')
plt.ylabel('PWM Output')
plt.show()
