import matplotlib.pyplot as plt
from numpy import *

class Agent:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "%s" % (self.name, )

class Manager(Agent):
    def __init__(self, name):
        Agent.__init__(self, name)
        self.children = []
        self.selected_agent = None
    def add_child(self, agent):
        self.children.append(agent)
        if self.selected_agent is None:
            self.selected_agent = agent
    def run(self):
        self.selected_agent.run()
        self.reconsider_selected_agent()
    def reconsider_selected_agent(self):
        other_agent = self.get_best_alternative()
        # MODIFY THIS LINE FOR CROSS EXCLUSION
        if self.selected_agent.get_status() < other_agent.get_status():
            self.selected_agent = other_agent
    def get_best_alternative(self):
        alternatives = [agent for agent in self.children if agent is not self.selected_agent]
        alternatives.sort(key=lambda x: x.get_status(), reverse=True)
        return alternatives[0]

    def get_status(self):
        # MODIFY THIS LINE FOR PRINCIPLE OF NONCOMPROMISE
        return self.selected_agent.get_status()

    def winner(self):
        return self.selected_agent.winner()

    def __str__(self):
        return "%s ==> %s" % (Agent.__str__(self), self.selected_agent, )

class Worker(Agent):
    def __init__(self, name, diff_eng, affect_resources):
        Agent.__init__(self, name)
        self.get_status = diff_eng
        self.run = affect_resources
    def winner(self):
        return self

class Resource:
    def __init__(self, value):
        self.value = value
    def incr(self, delta=1):
        self.value += delta
    def decr(self, delta=1):
        self.value -= delta
    def set(self, value):
        self.value = value
    def get(self):
        return self.value
    def __str__(self):
        return str(self.value)

def demo():
    
    # create resources
    nourishment = Resource(10)
    rest = Resource(10)
    blocks = Resource(0)

    # create different agents at play

    # top level agent
    child = Manager("child")

    # second tier agents
    eat = Worker("eat", 
                 lambda: 10 - nourishment.get(),
                 lambda: (nourishment.set(10), nourishment.incr()))
    play = Manager("play")
    sleep = Worker("sleep", 
                   lambda: (10 - rest.get()) / 6.0, 
                   lambda: (rest.set(10), blocks.set(0)))

    # third tier agents
    builder = Worker("builder",
                     lambda: max(0, 5 - blocks.get()),
                     lambda: blocks.set(min(blocks.get() + 1, 5)))
    wrecker = Worker("wrecker", 
                     lambda: blocks.get(),
                     lambda: blocks.set(0))
    
    # arrange agents in a hierarchy

    # connect first and second tier
    child.add_child(eat)
    child.add_child(play)
    child.add_child(sleep)
    child.selected_agent = play

    # connect second and third tier
    play.add_child(builder)
    play.add_child(wrecker)

    resource_history = []
    status_history = []
    winner_history = []

    time = 24

    for i in xrange(time):
        nourishment.decr()
        rest.decr()
        child.run()
        resource_history.append((nourishment.get(), rest.get(), blocks.get()))
        status_history.append([x.get_status() for x in (eat, sleep, builder, wrecker)])
        winner_history.append(child.winner())

    plt.figure(1)

    plt.subplot(311)
    plt.title("Resource History")
    plt.plot(resource_history)

    plt.subplot(312)
    plt.title("Status History")
    plt.plot(status_history)

    plt.subplot(313)
    plt.title("Active Agents")
    plt.xlim([0,time])
    plt.ylim([0,5])
    for i, winner in enumerate(winner_history):
        if i == 0 or winner is not winner_history[i-1]:
            plt.text(i, (builder, wrecker, eat, sleep).index(winner), str(winner))

    plt.savefig('som.png')


if __name__ == '__main__':
    demo()