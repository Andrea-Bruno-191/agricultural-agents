#!/usr/bin/python3

from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from labor_farm_worker import FarmWorker, get_total_workers, get_total_employed, get_total_documented
from labor_farm import Farm
import labor_utils as utils

# homeowner_states = ('landlord', 'dweller')

def find_event(evt_list, date_weeks):
    """Takes a list of (date, evt_str) pairs and returns today's
    event string if there is one; otherwise returns None"""
    for (date_weeks, evt_str) in evt_list:
        print(date_weeks, evt_str)
        if date_weeks == str(date_weeks):
            print('FOUND', evt_str)
            return evt_str
    return None

class CountyModel(Model):
    def __init__(self, N_fields, N_dwellers, width, height, seed=None):
        super().__init__(seed=seed)
        self.N_fields = N_fields
        self.N_dwellers = N_dwellers
        self.grid = MultiGrid(width, height, torus=True)
        self.date_weeks = 0
        self.running = True
        self.datacollector = DataCollector(
            model_reporters = {'W': get_total_workers,
                               'E': get_total_employed,
                               'D': get_total_documented
                               })
        self.init_fields()
        self.init_farm_workers()
        self.event_list = utils.load_chronology()

    def init_fields(self):
        """Create a certain number of houses, put them on the grid."""
        for i in range(self.N_fields):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            size = draw_from_powerlaw(exponent, ...)
            a = Farm(self, x, y, size, -1, -1)
            self.grid.place_agent(a, (x, y))

    def init_farm_workers(self):
        pass
        return
        # for i in range(self.N_fields):
        #     # start with all renters
        #     which_house = self.pick_random_empty_house()
        #     a = FarmWorker(self, False, which_house)
        #     self.current_id = i
        #     x = self.random.randrange(self.grid.width)
        #     y = self.random.randrange(self.grid.height)
        #     self.grid.place_agent(a, (x, y))
        #     # self.agents.add(a)

    def pick_random_empty_house(self):
        for a in self.agents:
            if isinstance(a, Farm) and a.owner_id == -1 and a.tenant_id == -1:
                return a
        raise Exception('no houses available')

    def step(self):
        self.date_weeks += 1
        today_event = find_event(self.event_list, self.date_weeks)
        print('TODAY_NEWS:', today_event)
        self.agents.shuffle_do('step')
        # self.schedule.step()
        self.datacollector.collect(self)
        # birth of new individuals?
        birth_rate = 0.02
        if self.random.random() < birth_rate:
            a = FarmWorker(self, 'W')
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            # self.schedule.add(a)
            print('#BIRTH:', a.unique_id, x, y)
