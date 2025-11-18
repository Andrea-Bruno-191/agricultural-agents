import math
from enum import Enum 
import mesa
from mesa.discrete_space import CellAgent

##current month is the global date, all agents are put in 
current_month = 1
current_year = 2022
BOGUS = -1

class WorKerStatus(Enum):
    """An immigrant farm worker who will come to the US
    but leave if wages are too low to compensate for
    concerns about immigration crackdown."""
    
    DOCUMTENTED = 1
    UNDOCUMENTED = 2
    DEPORTED = 3

class Worker(mesa.discrete_space.CellAgent):
    def __init__(self, model, fear, wage_threshold, 
    wage_constant): 
        """Create a new worker."""
        super().__init__(model)
        self.work_needed = BOGUS##function of the time of year, labor demand 
                            ##increases in summer and fall
        self.fear = 1 - math.exp(
            -1 * round(DEPORTED_COUNT / UNDOCUMENTED_COUNT))
        self.wage = work_needed / (DOCUMENTED_COUNT + UNDOCUMENTED_COUNT)
    ##function of work needed vs workers available. The wage offered.
        self.wage_threshold = self.wage_constant * (1 + self.fear)

        month = 0 
        work_needed = BOGUS
     

    def step(self):
        self.move()
        if self.wage_threshold >= self.wage: ##self deport 
            BOGUS
        def update_fear(self):
            print('I should update Fear') 

        def update_wage_threshold(self):
            print('I should update wages')
        

class ICE_officer(mesa.discrete_space.CellAgent):
    def __init__(self, model, vision, deportation):
        super().__init__(model)
        self.vision = BOGUS
        self.deportation = BOGUS

    def step(self):
        self.update_neighbors()
        active_neighbors = []
        for agent in self.neighbors: 
            if isinstance(agent, Worker) and agent.state == WorKerStatus.UNDOCUMENTED: 
                    undocumented_neighbors.append(agent)
            if undocumented_neighbors: 
                detainee = self.random.choice(undocumented_neighbors)
                detainee.state = WorkerStatus.DEPORTED
        self.move()
