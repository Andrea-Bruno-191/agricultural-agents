#!/usr/bin/python3

import random

from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


# infection_duration = 50         # how many steps before you either die or recover
# death_rate = 0.1
# immunity_duration = 100

# homeowner_states = ('landlord', 'dweller')

# neighborhood_foci = [(100, 100, 100),
#                      (100, 200, 130),
#                      (100, 300, 135),
#                      (200, 100, 120),
#                      (200, 200, 140),
#                      (200, 300, 155),
#                      (300, 100, 135),
#                      (300, 200, 148),
#                      (300, 300, 162),
#                      ]

# def generate_house_size(x, y):
#     """Generate an estimated house size (in square meters) for a given
#     neighborhood; this should depend on the average size in that neighborhood
#     with a 20% uniform variation."""
#     closest_focus_distance2 = ((neighborhood_foci[0][0] - x)**2
#                                + (neighborhood_foci[0][1] - y)**2)
#     closest_size = -1
#     for focus_x, focus_y, size in neighborhood_foci:
#         focus_distance2 = (focus_x - x)**2 + (focus_y - y)**2
#         if focus_distance2 < closest_focus_distance2:
#             closest_size = size
#     return size * (1 + (random.random() - 0.5) * 0.2)
                               

class DeportationAgency(Agent): # for example, in the US it could be ICE
    def __init__(self, model, x, y, owner_id, tenant_id):
        super().__init__(model)
        self.owner_id = owner_id
        self.tenant_id = tenant_id
        self.age = 0
        self.size_m2 = generate_house_size(x, y)
        self.current_mortgage = 0
        self.current_rent = 400

    def step(self):
        self.age += 1 # age is in time step units; not yet specified - maybe months?
        print(f"HOUSE: {self.unique_id} pos: {self.pos} owner: {self.owner_id}", end="")
        print(f"       tenant: {self.tenant_id} age: {self.age}")
        if self.owner_id == -1:
            self.look_for_buyer()
        # # then see if anyone dies or heals
        # if self.SIR_state == 'I' and self.infection_age > infection_duration:
        #     # print('#TIME_TO_DIE_OR_RETURN', self.infection_age)
        #     # decision time: after 50 days you either die or heal
        #     if self.random.random() < death_rate:
        #         print(f'#DEATH: {self.unique_id}, {self.pos}')
        #         # self.model.schedule.remove(self)
        #         self.remove()
        #         # print(dir(self.model.grid))
        #         # print(help(self.model.grid))
        #         # self.model.grid.remove_agent(self)
        #         # self.remove()
        #     else:
        #         self.SIR_state = 'R'
        #         self.infection_age = -1
        #         self.immunity_age = -1
        # # update the infection age
        # if self.SIR_state == 'I':
        #     self.infection_age += 1
        # if self.SIR_state == 'R':
        #     # if we're "removed" and still alive then we have
        #     # immunity, but the immunity can die after a while
        #     self.immunity_age += 1
        #     if self.immunity_age > immunity_duration:
        #         self.SIR_state = 'S' # return to the susceptible population
        #         self.immunity_age = -1
        #         print('#RETURN_TO_S: {self.unique_id}, {self.pos}')
        # if self.SIR_state == 'S': # examine possible spontaneous infection
        #     spontaneous_infection_rate = 0.0001
        #     if self.random.random() < spontaneous_infection_rate:
        #         print(f'#SPONTANEOUS_INFECTION: {self.unique_id}, {self.pos}')
        #         self.SIR_state = 'I'   # I become infected
        #         self.infection_age = 0 # track how long my infection has been

    def look_for_buyer(self):
        print(f'house {self.unique_id} is looking for a buyer')

    # def infect_neighbors(self):
    #     neighbors = self.model.grid.get_neighbors(self.pos,
    #                                               moore=True,
    #                                               include_center=True)
    #     for neighbor in neighbors:
    #         if neighbor.SIR_state == 'S' and self.random.random() < 0.25:
    #             # the infected dude infects this neighbor
    #             neighbor.SIR_state = 'I'
    #             # track how long they have had the infection
    #             neighbor.infection_age = 0
