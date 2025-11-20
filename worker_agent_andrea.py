import math
from enum import Enum 
import mesa

import farm_labor_model_andrea

##current month is the global date, all agents are put in 
current_month = 1
current_year = 2022
BOGUS = -1

class AgriModelAgent(mesa.discrete_space.CellAgent):
    def update_neighbors(self):
        self.neighborhood = self.cell.get_neighborhood(radius=self.vision)
        self.neighbors = self.neighborhood.agents
        self.empty_neighbors = [c for c in self.neighborhood if c.is_empty]
    
    def move(self):
        if self.model.movement and self.empty_neighbors: 
            new_pos = self.random.choice(self.empty_neighbors)
            self.move_to(new_pos)

class WorkerStatus(Enum):
    """An immigrant farm worker who will come to the US
    but leave if wages are too low to compensate for
    concerns about immigration crackdown."""
    DOCUMENTED = 1
    UNDOCUMENTED = 2
    DEPORTED = 3

class Worker(AgriModelAgent):
    def __init__(self, model, fear, wage_threshold, wage_baseline):
        """Create a new worker.
        Self.wage is the exogenous wage offered by firms, dependent
        on the amount of work needed and the number of workers available. 
        Wage_baseline is the standard base wage for an agricultural
        worker, close to $17/hr. 
        Wage_threshold is the wage the worker expects, contingent
        on their fear of being deported. 
        """
        super().__init__(model)
        self.status = WorkerStatus.DOCUMENTED
        self.model = model
        self.work_needed = work_needed
        ##function of the time of year, labor demand 
        ##increases in summer and fall
        self.fear = .01
        self.wage_baseline = wage_baseline
        self.wage = calc_wage(current_year, current_month, '96099',
                                         model.n_avail, wage_baseline)
        # self.fear = 1 - math.exp(
        #     -1 * round(DEPORTED_COUNT / UNDOCUMENTED_COUNT))
        # self.wage = work_needed / (DOCUMENTED_COUNT + UNDOCUMENTED_COUNT)
        ##function of work needed vs workers available. The wage offered.
        self.wage_threshold = self.wage_baseline * (self.fear)
        self.empty_neighbors = []
     
    def step(self):
        """Update fear and wage threshold, 
        decide whether to leave or stay in the USA."""
        self.update_fear()
        self.update_wage_threshold()

        self.move()
        if self.wage_threshold >= self.wage: 
            self.state = WorkerStatus.DEPORTED

        self.fear = self.fear * (.8 + DEPORTED / UNDOCUMENTED) #Aim to make this fluctuate around 1 

        self.wage_threshold = self.wage_threshold * (self.fear) #Should fluctuate but generally increase 
        

class ICE_officer(AgriModelAgent):
    def __init__(self, model, vision, deportation):
        super().__init__(model)
        self.vision = vision
        self.deportation = deportation
        self.undocumented_neighbors = []

    def step(self):
        self.update_neighbors()
        undocumented_neighbors = []
        for agent in self.neighbors: 
            if isinstance(agent, Worker) and agent.status == WorkerStatus.UNDOCUMENTED: 
                self.undocumented_neighbors.append(agent)
            if self.undocumented_neighbors: 
                detainee = self.random.choice(self.undocumented_neighbors)
                detainee.status = WorkerStatus.DEPORTED
        self.move()
