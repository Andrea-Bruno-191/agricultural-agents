#!/usr/bin/python3

import random

from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


infection_duration = 50         # how many steps before you either die or recover
death_rate = 0.1
immunity_duration = 100

homeowner_states = ('landlord', 'dweller')

neighborhood_foci = [(100, 100, 100),
                     (100, 200, 130),
                     (100, 300, 135),
                     (200, 100, 120),
                     (200, 200, 140),
                     (200, 300, 155),
                     (300, 100, 135),
                     (300, 200, 148),
                     (300, 300, 162),
                     ]

def generate_farm_size(x, y):
    """Generate an estimated house size (in square meters) for a given
    neighborhood; this should depend on the average size in that neighborhood
    with a 20% uniform variation."""
    closest_focus_distance2 = ((neighborhood_foci[0][0] - x)**2
                               + (neighborhood_foci[0][1] - y)**2)
    closest_size = -1
    for focus_x, focus_y, size in neighborhood_foci:
        focus_distance2 = (focus_x - x)**2 + (focus_y - y)**2
        if focus_distance2 < closest_focus_distance2:
            closest_size = size
    return size * (1 + (random.random() - 0.5) * 0.2)
                               

class Farm(Agent):
    def __init__(self, model, x, y, owner_id, tenant_id):
        super().__init__(model)
        self.product_list = ['lettuce']
        self.product_data = {'lettuce' : 0}
        self.size_m2 = generate_farm_size(x, y)
        self.current_mortgage = 0
        self.current_rent = 400
        self.owner_id = 1

    def step(self):
        # self.age += 1 # age is in time step units; not yet specified - maybe months?
        print(f"HOUSE: {self.unique_id} pos: {self.pos} owner: {self.owner_id}", end="")
        # print(f"       tenant: {self.tenant_id} age: {self.age}")
        if self.owner_id == -1:
            self.look_for_buyer()

    def look_for_buyer(self):
        print(f'house {self.unique_id} is looking for a buyer')
