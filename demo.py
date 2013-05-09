from model import *
import matplotlib.pyplot as plt

'''
Copyright (c) 2013 Joseph Henke
See LICENSE for licensing information

'''

# Parameters of the Model
timesteps = 24

CROSS_EXCLUSION_FACTOR = 3

def DIFFICULTY_ENGINE(selected_agent, all_agents):
    return 0

MAX_BUILD_SIZE = 5

MAX_NOURISHMENT = 10
MAX_REST = 10
REST_DECR = 0.15

INITIAL_NOURISHMENT = MAX_NOURISHMENT
INITIAL_REST = MAX_REST
INITIAL_BLOCKS = 0

# create resources
nourishment = Resource(INITIAL_NOURISHMENT)
rest = Resource(INITIAL_REST)
blocks = Resource(INITIAL_BLOCKS)

# create different agents at play

# top level agent
child = Manager("child")

# second tier agents
eat = Worker("eat", 
             lambda: MAX_NOURISHMENT - nourishment.get(),
             lambda: (nourishment.set(MAX_NOURISHMENT), nourishment.incr()))
play = Manager("play", 
               difficulty_engine = DIFFICULTY_ENGINE,
               cross_exclusion = CROSS_EXCLUSION_FACTOR)
sleep = Worker("sleep", 
               lambda: MAX_REST - rest.get(), 
               lambda: (rest.set(MAX_REST), blocks.set(0)))

# third tier agents
builder = Worker("builder",
                 lambda: max(0, MAX_BUILD_SIZE - blocks.get()),
                 lambda: blocks.set(min(blocks.get() + 1, MAX_BUILD_SIZE)))
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

for i in xrange(timesteps):
    nourishment.decr()
    rest.decr(REST_DECR)
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
plt.xlim([0,timesteps])
plt.ylim([0,5])
for i, winner in enumerate(winner_history):
    if i == 0 or winner is not winner_history[i-1]:
        plt.text(i, (builder, wrecker, eat, sleep).index(winner), str(winner))

plt.savefig('som.png')