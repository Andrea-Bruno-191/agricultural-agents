import math
from enum import Enum 
import mesa
from mesa.discrete_space import CellAgent

class WorKerStatus(Enum):
    """An immigrant farm worker who seeks high-wage employment,
    subject to concerns about immigration crackdown."""
    DOCUMTENTED = 1
    UNDOCUMENTED = 2
    DEPORTED = 3



class Worker(mesa.discrete_space.CellAgent):
    def 


def __init__(self, model, fear, wage, wage_threshold): 
    """Create a new worker."""
    super().__init__(model)
    self.cell = cell 
    self.fear = ##(random number between 0 and 1)*number of deported * documented status
    self.wage = ##function of work needed vs workers available 
    self.wage_threshold = ##function of fear, hazard dynamic

def step(self):
    self.move()
    if self.wage_threshold >= self.wage ##self deport  

class ICE_officer(CellAgent)
def __init__(self, model, vision, deportation):
super().__init__(model)
self.vision = vision 
self.deportation = deportation

def step(self):
    self.update_neighbors()
    active_neighbors = []
    for agent in self.neighbors: 
        if isinstance(agent, Worker) and Worker.state = WorKerStatus.UNDOCUMENTED: ##Wait. Documentation status doesn't change, so maybe alter this?    
                    undocumented_neighbors.append(agent)
        if undocumented_neighbors: 
            detainee = self.random.choice(undocumented_neighbors)
            detainee.state = WorkerStatus.DEPORTED

    self.move()