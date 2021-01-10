# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 13:31:13 2020

@author: vmmb29
"""

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

def compute_InfPercent(model):
    agent_states = [agent.state for agent in model.schedule.agents]
    return sum(agent_states)/len(agent_states)

class InfectionAgent(Agent):
    """An agent with initial susceptibility."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
        # 0=S, 1=I, 2=R
        self.infection_time = 0
        self.recovered_time = 0
        
        if self.unique_id == 0:
            self.state = 1
        else:
            self.state = 0
            

        # print('state: ',self.state)
    def step(self):
        # agent step
        if self.state ==1:
            self.infection_time +=1
        elif self.state==2:
            self.recovered_time+=1
            
        if self.infection_time >=10:
            self.state = 2
            self.infection_time=0
            
        if self.recovered_time >=10:
            self.state = 0
            self.recovered_time = 0
            
        self.move()
        if self.state == 1:
            self.infect()
        
    def move(self):
        if not 'self.bubble' in locals():
            print('no bubble')
            self.bubble = 
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore = False,
            include_center = True)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        
    def infect(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates)>1:
            for other in cellmates:
                if other.state == 0:
                    other.state = 1

        
        
class InfectionModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height, bubble_size = 3):
        self.num_agents = N
        self.grid = MultiGrid(width,height, True)
        self.schedule = RandomActivation(self)
        self.bubble_size = 3
        # Create agents
        for i in range(self.num_agents):
            a = InfectionAgent(i, self)
            self.schedule.add(a)
            
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x,y))
            
        self.datacollector = DataCollector(
            model_reporters = {"InfPerc":compute_InfPercent},
            agent_reporters = {"state":"state"})
    
    def step(self):
        self.datacollector.collect(self)
        # advance model by one step/tick
        self.schedule.step()