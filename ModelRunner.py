# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 13:41:08 2020

@author: vmmb29
"""

from InfectionModelandAgent import InfectionModel
import matplotlib.pyplot as plt

model = InfectionModel(50,10,10)
num_steps = 100
num_infected = [0]*num_steps
num_removed = [0]*num_steps
num_susceptible = [0]*num_steps
for i in range(num_steps):
    model.step()
    agent_states = [a.state for a in model.schedule.agents]
    num_infected[i]=agent_states.count(1)
    num_removed[i] = agent_states.count(2)
    num_susceptible[i] = agent_states.count(0)
    
    
#agent_states = [a.state for a in model.schedule.agents]
plt.plot(num_infected)
plt.plot(num_removed)
plt.plot(num_susceptible)

#%%
import numpy as np

agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    agent_count = len(cell_content)
    agent_counts[x][y] = agent_count
plt.imshow(agent_counts,interpolation='nearest')
plt.colorbar()