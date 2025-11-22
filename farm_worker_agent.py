""" 
Agricultural labor model - definitions of agents. 

We define two agent classes here, Worker and ICE_Agent.

These will typically be created by methods in a model object.

"""


import math
from enum import Enum
import mesa

import random

class WorkerStatus(Enum):
    """An immigrant farm worker who will come to the US
    but leave if wages are too low to compensate for
    concerns about immigration crackdown."""
    DOCUMENTED = 1
    UNDOCUMENTED = 2
    DEPORTED = 3

#
def calc_n_deported(model):
    n_deported = 0
    print(len(model.agents_by_type[Worker]))
    for agent in model.agents_by_type[Worker]:
        # print("THIS_AGENT:", agent.unique_id, agent.status)
        if agent.status == WorkerStatus.DEPORTED:
            n_deported += 1
    return n_deported

#Now three functions that scan all the agents to sum up how many 
#workers are in each status. 
def calc_n_undocumented(model):
    n_undocumented = 0
    print(len(model.agents_by_type[Worker]))
    for agent in model.agents_by_type[Worker]:
        # print("THIS_AGENT:", agent.unique_id, agent.status)
        if agent.status == WorkerStatus.UNDOCUMENTED:
            n_undocumented += 1
    return n_undocumented

def calc_n_workers(model):
    n_workers = 0
    print(len(model.agents_by_type[Worker]))
    for agent in model.agents_by_type[Worker]:
        # print("THIS_AGENT:", agent.unique_id, agent.status)
        if agent.status != WorkerStatus.DEPORTED:
            n_workers += 1
        return n_workers



class AgriModelAgent(mesa.discrete_space.CellAgent):
    """Base class for both types of agents: Workers and ICE officers."""
    def update_neighbors(self):
        """If I've moved or if my vision has changed, I'll need to 
        recalculate my neighborhood!"""
        self.neighborhood = self.cell.get_neighborhood(radius=self.vision)
        self.neighbors = self.neighborhood.agents
        self.empty_neighbors = [c for c in self.neighborhood if c.is_empty]

    def move(self):
        """Pick a random location among my neighbors and move there."""
        if self.model.movement and self.empty_neighbors:
            new_pos = self.random.choice(self.empty_neighbors)
            self.move_to(new_pos)

class Worker(AgriModelAgent):
    """Worker agent - derives from AgriModelAgent and adds to it a 
    representation of fear, immigration status, and wage threshold."""
    def __init__(self, model, fear):
        """Create a new worker.
        Self.wage is the exogenous wage offered by firms, dependent
        on the amount of work needed and the number of workers available.
        Wage_baseline is the standard base wage for an agricultural
        worker, close to $17/hr.
        Wage_threshold is the wage the worker expects, contingent
        on their fear of being deported.
        """
        super().__init__(model)
        # 
        self.model = model
        self.status = WorkerStatus.DOCUMENTED if random.random() < 0.6 else WorkerStatus.UNDOCUMENTED
        self.fear = 1.0 + 0.1 * (2 * random.random() - 1) 
        #wage_threshold is the lowest wage an agent will accept
        #before leaving the country. Initial value is set to 
        #wage baseline in the model. 
        self.wage_threshold = self.model.wage_baseline 
        self.empty_neighbors = []

    def step(self):
        """Update fear and wage threshold,
        decide whether to leave or stay in the USA."""
        if self.wage_threshold >= self.model.wage:
            self.state = WorkerStatus.DEPORTED
        # Aim to make this fluctuate around 1
        n_deported = calc_n_deported(self.model)
        n_undocumented = calc_n_undocumented(self.model)
        #Now calculate the fear factor. The algorithm is rudimentary
        #and will be further refined. Right now: 
        #If I'm documented, fear = 0
        #If I'm undocumented, it depends on the ratio of deportations
        #to other undocumented immigrants. 
        #Prevents from dividing by zero! 
        if self.status == WorkerStatus.DOCUMENTED: 
            self.fear = 0 
        elif n_undocumented == 0:
            self.fear = 0
        else:
            self.fear = self.fear * (.8 + n_deported / n_undocumented)
        # Should fluctuate but generally increase
        self.wage_threshold = self.wage_threshold * self.fear
        self.vision = 1 
        self.update_neighbors()
        self.move()

    def handle_immigration(self, n_employed, n_jobs_offered,
                           n_total_workers, n_unemployed):
        """Note: not yet in use! Will soon represent agents moving into the 
        USA. Immigration can probably be simulated in a sophisticated
        manner.  For now I just do it as a probability of people
        moving in or out based on the job situation.

        """
        n_people_move_in = round(utils.global_state['immigration_max_weekly']
                                 * (2*expit(0.1*wage)))
        print('handle_immigration:', wage,
              ' -- ', n_people_move_in)
        if n_people_move_in > 0:
            for i in range(n_people_move_in):
                WorkerStatus.DOCUMENTED = True if random.random() < 0.7 else False
                self.grid.place_agent(Worker, Worker.get_coords())
                print('NEW_AGENT:', Worker.unique_id)
        print(f'GET_STUFF_AFTER_IMMIGRATION_{self.steps}:'
              + f' tot: {get_total_workers(self)} - employed:'
              + f' {get_total_employed(self)} docu: {get_total_documented(self)}')


class ICE_Officer(AgriModelAgent):
    def __init__(self, model, vision):
        """Main argument is "vison" which is how far from my cell do
        I look to try to find immigrants. A sort of radius which is 
        correlated with enforcement aggressiveness."""
        super().__init__(model)
        self.vision = vision
        self.undocumented_neighbors = []

    def step(self):
        """We round up undocumented neighbors and then move to another cell.
        """
        self.update_neighbors()
        self.undocumented_neighbors = []
        for agent in self.neighbors:
            if isinstance(agent, Worker) and agent.status == WorkerStatus.UNDOCUMENTED:
                self.undocumented_neighbors.append(agent)
            if self.undocumented_neighbors:
                detainee = self.random.choice(self.undocumented_neighbors)
                detainee.status = WorkerStatus.DEPORTED
        self.move()
