from model import *
from random import random
import matplotlib.pyplot as plt
from pylab import *

'''
Copyright (c) 2013 Joseph Henke
See LICENSE for licensing information

'''

# Parameters of the Model


def simulate(DIFFICULTY_FACTOR=0, CROSS_EXCLUSION_FACTOR=0):
    '''
    Runs a simulation of 24 timesteps and return the history

    @DIFFICULTY_FACTOR determines how much the conflict within an agent is 
        considered in choosing which agent to be active.
    @CROSS_EXCLUSION_FACTOR detrmines by how much an unselected_agent's Status
        must be beyond the currently selected_agent to change to that

    @returns a dictionary recording the history of run
        keys - idenifying poperty
        values - the list of the values of that property at each time step

    '''

    # Setup

    timesteps = 24

    def DIFFICULTY_ENGINE(selected_agent, all_agents):
        distro = [x.get_status() for x in all_agents]
        mean = sum(distro) / len(distro)
        top = max(distro)
        var_from_max = sum([(top - x)**2 for x in distro]) / len(all_agents)
        # return DIFFICULTY_FACTOR/abs(all_agents[0].get_status() - all_agents[1].get_status())
        return DIFFICULTY_FACTOR / (1+var_from_max)

    MAX_BUILD_SIZE = 5

    MAX_NOURISHMENT = 10
    MAX_REST = 2
    REST_DECR = 0.3

    # randomness is chosen to start to avoid exact equalities
    INITIAL_NOURISHMENT = MAX_NOURISHMENT - random()
    INITIAL_REST = MAX_REST - random()
    INITIAL_BLOCKS = 1 - random()

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
                   lambda: (rest.set(MAX_REST), ))

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

    history = {'eat':[], 
               'play': [], 
               'builder': [], 
               'wrecker': [], 
               'sleep': [], 
               'winner': [], 
               'child_selected': [],
               'nourishment': [],
               'rest': [],
               'blocks': [],
               'play_conflict': []}

    for i in xrange(timesteps):

        # run agents
        child.run()

        # affect time senstivie resources
        nourishment.decr()
        rest.decr(REST_DECR)

        # record history
        history['winner'].append(child.winner().name)
        history['child_selected'].append(child.selected_agent.name)
        history['eat'].append(eat.get_status())
        history['play'].append(play.get_status())
        history['builder'].append(builder.get_status())
        history['wrecker'].append(wrecker.get_status())
        history['sleep'].append(sleep.get_status())
        history['play_conflict'].append(play.get_conflict())
        history['nourishment'].append(nourishment.get())
        history['rest'].append(rest.get())
        history['blocks'].append(blocks.get())

    return history

# create images for paper

'''Basic Visualization'''
history = simulate()
plt.figure(1, figsize=(12,8))
plt.subplot(211)
plt.title("Agency Resources", size="xx-large")
plt.xlabel("Time")
plt.plot(history['nourishment'], label="food")
plt.plot(history['rest'], label="rest")
plt.plot(history['blocks'], label="blocks")
plt.legend()

plt.subplot(212)
plt.title("Worker Agent Statuses", size="xx-large")
plt.xlabel("Time")
plt.plot(history['eat'], label="eat")
plt.plot(history['wrecker'], label="wrecker")
plt.plot(history['builder'], label="builder")
plt.plot(history['sleep'], label="sleep")
for i, name in enumerate(history['winner']):
    plt.text(i, history[name][i], name, ha="center")
plt.legend()
plt.tight_layout()
plt.savefig("basic_vis.png")

'''Difficulty Detracts from Playtime'''
percentages = []
diff_factors = (0, 1.0, 2.0, 3.0, 4.0, 5.0)
for i in diff_factors:
    history = simulate(i)
    distro = history['child_selected']
    num_play = sum([1 for x in distro if x == 'play'])
    percentages.append(1.0 * num_play / len(distro))
plt.figure(2, figsize=(8,6))
plt.title("Conflict Within Play Decreases Play's Total Time", size="xx-large")
plt.xlabel("Degree to Which Conflict Detracts from Agent's Status")
plt.ylabel("Percentage of Day Spent Playing")
plt.plot(diff_factors, percentages)
plt.tight_layout()
plt.savefig("difficulty_lessens_time.png")

'''Difficulty Is Related to the Shared Resource - Block Height'''
plt.figure(3, figsize=(8,6))
plt.title("Difficulty and Block Height", size="xx-large")
plt.xlabel("Block Height")
plt.ylabel("Conflict")
history = simulate(0.5)
plt.scatter(history['blocks'], history['play_conflict'], label="Play's Internal Conflict")
plt.savefig("conflict_and_block_height.png")


'''Cross Exclusion Factor Reduces Build/Wreck Cycle'''
plt.figure(4, figsize=(12,8))
plt.subplot(211)
plt.title("Block Heights With No Cross Exclusion", size="xx-large")
plt.xlabel("Time")
plt.ylabel("Height of Blocks")
plt.ylim([0,6])
history = simulate()
plt.plot(history['blocks'])

plt.subplot(212)
plt.title("Block Heights With Cross Exclusion", size="xx-large")
plt.xlabel("Time")
plt.ylabel("Height of Blocks")
history = simulate(0,3)
plt.plot(history['blocks'])
plt.ylim([0,6])
plt.tight_layout()
plt.savefig("cross_exclusion.png")
























