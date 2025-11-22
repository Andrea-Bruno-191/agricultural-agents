import math
from enum import Enum
import mesa
import random

BOGUS = -1

visa_access = random.randint(0, 10)

class WorkerStatus(Enum):
    """An immigrant farm worker who will come to the US
    but leave if wages are too low to compensate for
    concerns about immigration crackdown."""
    DOCUMENTED = 1
    UNDOCUMENTED = 2
    DEPORTED = 3


def calc_n_deported(model):
    n_deported = 0
    print(len(model.agents_by_type[Worker]))
    for agent in model.agents_by_type[Worker]:
        # print("THIS_AGENT:", agent.unique_id, agent.status)
        if agent.status == WorkerStatus.DEPORTED:
            n_deported += 1
    return n_deported

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
    def update_neighbors(self):
        self.neighborhood = self.cell.get_neighborhood(radius=self.vision)
        self.neighbors = self.neighborhood.agents
        self.empty_neighbors = [c for c in self.neighborhood if c.is_empty]

    def move(self):
        if self.model.movement and self.empty_neighbors:
            new_pos = self.random.choice(self.empty_neighbors)
            self.move_to(new_pos)

class Worker(AgriModelAgent):
    def __init__(self, model, fear, wage_threshold, doc_tag):
        """Create a new worker.
        Self.wage is the exogenous wage offered by firms, dependent
        on the amount of work needed and the number of workers available.
        Wage_baseline is the standard base wage for an agricultural
        worker, close to $17/hr.
        Wage_threshold is the wage the worker expects, contingent
        on their fear of being deported.
        """
        super().__init__(model)
        # self.doc_tag = random.randint(0, 100)
        self.status = WorkerStatus.DOCUMENTED if random.random() < 0.6 else WorkerStatus.UNDOCUMENTED
        self.model = model
        # self.labor_needed = labor_needed
        ##function of the time of year, labor demand
        ##increases in summer and fall
        self.fear = 0.01
        # self.fear = 1 - math.exp(
        #     -1 * round(DEPORTED_COUNT / UNDOCUMENTED_COUNT))
        # self.wage = work_needed / (DOCUMENTED_COUNT + UNDOCUMENTED_COUNT)
        ##function of work needed vs workers available. The wage offered.
        self.wage_threshold = self.model.wage_baseline * (self.fear)
        self.empty_neighbors = []

    def step(self):
        """Update fear and wage threshold,
        decide whether to leave or stay in the USA."""
        self.move()
        if self.wage_threshold >= self.model.wage:
            self.state = WorkerStatus.DEPORTED
        # Aim to make this fluctuate around 1
        n_deported = calc_n_deported(self.model)
        n_undocumented = calc_n_undocumented(self.model)
        print("=========== n_deported:", n_deported)
        print("=========== n_undocumented:", n_undocumented)
        if n_undocumented == 0:
            self.fear = 0
        else:
            self.fear = self.fear * (.8 + n_deported / n_undocumented)
        # Should fluctuate but generally increase
        self.wage_threshold = self.wage_threshold * (self.fear)

    def handle_immigration(self, n_employed, n_jobs_offered,
                           n_total_workers, n_unemployed):
        """Immigration can probably be simulated in a sophisticated
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


class ICE_officer(AgriModelAgent):
    def __init__(self, model, vision, deportation):
        super().__init__(model)
        self.vision = vision
        self.deportation = deportation
        self.undocumented_neighbors = []

    def step(self):
        self.update_neighbors()
        self.undocumented_neighbors = []
        for agent in self.neighbors:
            if isinstance(agent, Worker) and agent.status == WorkerStatus.UNDOCUMENTED:
                self.undocumented_neighbors.append(agent)
            if self.undocumented_neighbors:
                detainee = self.random.choice(self.undocumented_neighbors)
                detainee.status = WorkerStatus.DEPORTED
        self.move()
