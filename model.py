'''
Copyright (c) 2013 Joseph Henke
See LICENSE for licensing information

'''

class Agent:
    ''' 
    This is the base class to represent an agent.

    Agent objects should be instantiated as one the subclasses.

    '''
    
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return "%s" % (self.name, )

class Manager(Agent):
    
    def __init__(self, name, difficulty_engine=lambda a,b:0, cross_exclusion=0):
        '''
        A Manager Agent is intended to model an agent which delegates work.

        @name - a string to help identify this agent
        @difficulty_engine - a function which takes two arguments,
                1) this Agent's selected agent
                2) this Agent's childrens
            and returns a number indicating the conflict of this Agent.
            higher conflict should produce a higher value.
        @cross_exclusion - the amount by which an unselected agent's status
            must be greater than this Agent's selected agent to become selected.

        '''
        Agent.__init__(self, name)
        self.children = []
        self.selected_agent = None
        self.difficulty_engine = difficulty_engine
        self.cross_exclusion = cross_exclusion
    
    def add_child(self, agent):
        '''add the given Agent as a child of this agent'''
        self.children.append(agent)
        if self.selected_agent is None:
            self.selected_agent = agent
    
    def run(self):
        '''runs the selected agent and recomputes the selected agent'''
        self.selected_agent.run()
        self.reconsider_selected_agent()

    def reconsider_selected_agent(self):
        '''recomputes which agent is selected'''
        other_agent = self.get_best_alternative()
        if self.selected_agent.get_status() + self.cross_exclusion < other_agent.get_status():
            self.selected_agent = other_agent
    
    def get_best_alternative(self):
        '''helper function to determine the best alternative to the selected agent'''
        alternatives = [agent for agent in self.children if agent is not self.selected_agent]
        alternatives.sort(key=lambda x: x.get_status(), reverse=True)
        return alternatives[0]

    def get_status(self):
        '''returns the status of this agent, taking into account its internal conflict'''
        return self.selected_agent.get_status() -\
            self.difficulty_engine(self.selected_agent, self.children)

    def get_conflict(self):
        '''returns the conflict within this agent'''
        return self.difficulty_engine(self.selected_agent, self.children)

    def winner(self):
        '''this is a helper function to determine which worker node is currently selected.'''
        return self.selected_agent.winner()

    def __str__(self):
        return "%s ==> %s" % (Agent.__str__(self), self.selected_agent, )

class Worker(Agent):

    def __init__(self, name, diff_eng, affect_resources):
        '''
        A Worker Agent is intended to model an agent which actually affects resources

        @name - a string to identify this Agent
        @diff_eng - this is the difference engine which gives this agent it status
            it is an function of no arguments
        @affect_resources - this is a function of no argumets, which mutates the 
            resources for when this agent is selected and run

        NOTE: affect_resources should behave in such a way as to reduce 
              the output of diff_eng

        '''
        Agent.__init__(self, name)
        self.get_status = diff_eng
        self.run = affect_resources
    
    def winner(self):
        '''end of recursion in finding which worker node is selected'''
        return self

class Resource:
    '''
    A resource simply represents a shared, mutable value within an Agency.

    It methods should be self explanatory.
    
    '''
    
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
