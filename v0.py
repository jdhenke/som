import math
from random import random
from pylab import *
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1.0 / (1.0 + (math.e ** (0.0-x)))

class Agent:
    def __init__(self):
        self.history = []
    def incr(self):
        pass
    def decr(self):
        pass

class IncreasingAgent(Agent):
    def __init__(self, rate = 0):
        Agent.__init__(self)
        self.rate = rate
        self.x = 0
    def get_level(self):
        return sigmoid(self.x)
    def incr(self):
        self.x += self.rate
    def decr(self):
        self.x -= self.rate

class ConstantAgent(Agent):
    def __init__(self, level = 0.5):
        Agent.__init__(self)
        self.level = level
    def get_level(self):
        return self.level

def timer(agents):
    def output():
        for agent in agents:
            agent.history.append(agent.get_level())
    return output

def v3():
    plt.figure(1)
    plt.subplot(211)
    history = []
    agents = [random(),random(),random()]    
    for i in xrange(10):
        agents = [x**0.75 for x in agents]
        total = sum(agents)
        agents = [x / total for x in agents]
        history.append(agents)
    plt.plot(history)
    plt.subplot(212)
    plt.text(0,0,"joe") 
    plt.savefig("som.png")

def v2():
    eat = IncreasingAgent(rate=0.6)
    sleep = IncreasingAgent(rate=0.1)
    play = ConstantAgent(level=0.5)
    agents = [eat, play, sleep]
    update = timer(agents)
    for i in xrange(20):
        agents.sort(key=lambda x: x.get_level(), reverse=True)
        agents[0].decr(0.1)
        for agent in agents[1:]:
            agent.incr()
        update()
    plot(eat.history)
    plot(play.history)
    plot(sleep.history)
    savefig("som.png")



def v1():
    eat = Agent()
    play = Agent()
    sleep = Agent()

    agents = [eat, play, sleep]

    for i in xrange(10):
        agents.sort(key=lambda x: x.get_level(), reverse=True)
        agents[0].decr(random()*0.1)
        for agent in agents[1:]:
            agent.incr(random()*0.1)
    plot(eat.history)
    plot(play.history)
    plot(sleep.history)
    savefig("som.png")

def v0():
    ''''''
    eat = Agent()
    play = Agent()

    current_agent = eat
    other_agent = play
    for i in xrange(100):
        if other_agent.get_level() > current_agent.get_level() + random():
            current_agent, other_agent = other_agent, current_agent

        current_agent.decr(0.15* random())
        other_agent.incr(0.1 * random())

    plot(eat.history)
    plot(play.history)
    savefig("som.png")

if __name__ == '__main__':

    text(4, 0.5,"joe")
    v3()
