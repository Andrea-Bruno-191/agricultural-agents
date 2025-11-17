#!/usr/bin/python3

import numpy as np

from mesa import Model 
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalMooreGrid 
from mesa.experimental.continuous_space import ContinuousSpaceAgent 


from worker_agent_andrea import current_month, current_year


class agricultural_model(Model):
    def __init__(
        self, 
        width = 40,
        height = 40,
        worker_density = 0.7, 
        ICE_density = 0.5
    ):
        print('agricultural model init')
    def step(self):
        current_month = current_month + 1
        if current_month > 12:
            current_month = 1
            current_year += 1 
        print(current_year, current_month)

