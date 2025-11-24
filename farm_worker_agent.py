""" 
Agricultural labor model - definitions of agents. 

We define two agent classes here, Worker and ICE_Agent.

These will typically be created by methods in a model object.

"""


import math
from enum import Enum
import mesa
from scipy.special import expit

import random

class WorkerStatus(Enum):
    """An immigrant farm worker who will come to the US
    but leave if wages are too low to compensate for
    concerns about immigration crackdown."""
    DOCUMENTED = 1
    UNDOCUMENTED = 2
    DEPORTED = 3
    DOCUMENTED_LEAVING = 4

#
def calc_n_deported(model):
    n_deported = 0
    #print(len(model.agents_by_type[Worker]))
    for agent in model.agents_by_type[Worker]:
        # print("THIS_AGENT:", agent.unique_id, agent.status)
        if agent.status == WorkerStatus.DEPORTED:
            n_deported += 1
    return n_deported

#Now three functions that scan all the agents to sum up how many 
#workers are in each status. 
def calc_n_undocumented(model):
    n_undocumented = 0
    #print(len(model.agents_by_type[Worker]))
    for agent in model.agents_by_type[Worker]:
        # print("THIS_AGENT:", agent.unique_id, agent.status)
        if agent.status == WorkerStatus.UNDOCUMENTED:
            n_undocumented += 1
    return n_undocumented

def calc_n_workers(model):
    n_workers = 0
    #print(len(model.agents_by_type[Worker]))
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
    def __init__(self, model):
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
        wage_positivity_factor = 0.05
        wage_positivity = self.model.wage - self.model.wage_baseline

        prob_documented = expit(wage_positivity * wage_positivity_factor) 
        self.status = WorkerStatus.DOCUMENTED if random.random() < prob_documented else WorkerStatus.UNDOCUMENTED
        self.fear = 1.0 + 0.1 * (2 * random.random() - 1) 
        #wage_threshold is the lowest wage an agent will accept
        #before leaving the country. Initial value is set to 
        #wage baseline in the model. 
        self.wage_threshold = self.model.wage_baseline 
        self.empty_neighbors = []
        self.choose_if_I_leave_documented()
        self.choose_if_I_leave_undocumented()

    def step(self):
        """Update fear and wage threshold,
        decide whether to leave or stay in the USA."""
        #Now handle if this agent wants to leave. This will
        #be different if they're documented, based on wages, 
        #or undocumented, based on fear and wages. 
        if self.status == WorkerStatus.DOCUMENTED: 
            self.choose_if_I_leave_documented()
        elif self.status == WorkerStatus.UNDOCUMENTED:
            self.choose_if_I_leave_undocumented()

        self.wage_threshold = self.wage_threshold * self.fear
        self.vision = 1 
        self.update_neighbors()
        self.move()

    def choose_if_I_leave_documented(self):
        """A documented worker will leave if they are not paid enough.
    Another factor is the overall climate regarding immigrants,
    represented by ICE aggression."""
        leaving_mobility_factor = 0.5
        sigmoid_arg = (self.model.wage_baseline - self.model.wage -2) * leaving_mobility_factor
        outgoing_prob = expit(sigmoid_arg)
        print("DOC_OUT: Wage, wage_baseline:", self.model.wage, 
        self.model.wage_baseline)
        print("DOC_OUT: prob, outgoing:", outgoing_prob)
        if random.random() < outgoing_prob: 
            self.status = WorkerStatus.DOCUMENTED_LEAVING
            print("DOC_OUT: GONEZO")

    def choose_if_I_leave_undocumented(self): 
        if self.wage_threshold >= self.model.wage:
            self.state = WorkerStatus.DEPORTED
        n_deported = calc_n_deported(self.model)
        n_undocumented = calc_n_undocumented(self.model)
        if n_undocumented == 0: 
            self.fear = 0
        else:
            self.fear = self.fear * (.8 + n_deported / n_undocumented)


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
