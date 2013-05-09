'''
Copyright (c) 2013 Joseph Henke
See LICENSE for licensing information

'''

class Agent:
    
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return "%s" % (self.name, )

class Manager(Agent):
    
    def __init__(self, name, difficulty_engine=lambda a,b:0, cross_exclusion=0):
        Agent.__init__(self, name)
        self.children = []
        self.selected_agent = None
        self.difficulty_engine = difficulty_engine
        self.cross_exclusion = cross_exclusion
    
    def add_child(self, agent):
        self.children.append(agent)
        if self.selected_agent is None:
            self.selected_agent = agent
    
    def run(self):
        self.selected_agent.run()
        self.reconsider_selected_agent()
    
    def reconsider_selected_agent(self):
        other_agent = self.get_best_alternative()
        if self.selected_agent.get_status() + self.cross_exclusion < other_agent.get_status():
            self.selected_agent = other_agent
    
    def get_best_alternative(self):
        alternatives = [agent for agent in self.children if agent is not self.selected_agent]
        alternatives.sort(key=lambda x: x.get_status(), reverse=True)
        return alternatives[0]

    def get_status(self):
        return self.selected_agent.get_status() -\
            self.difficulty_engine(self.selected_agent, self.children)

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
