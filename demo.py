from model import *
import matplotlib.pyplot as plt

'''
Copyright (c) 2013 Joseph Henke
See LICENSE for licensing information

'''

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