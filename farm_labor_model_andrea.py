#!/usr/bin/python3

import numpy as np
import mesa
from mesa import Model 
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalMooreGrid 
from mesa.experimental.continuous_space import ContinuousSpaceAgent 


from worker_agent_andrea import current_month, current_year, WorkerStatus, worker, ICE_officer


class agricultural_model(Model):
    def __init__(
        self, 
        width = 40,
        height = 40,
        worker_density = 0.7, 
        ICE_density = 0.05,
        ICE_vision = 5,
        movement=True,
        seed=None,
        max_iters=1000
    ):
        super().__init__(seed=seed)
        self.movement = movement
        self.max_iters = max_iters
        
        
        self.grid = mesa.discrete_space.OrthogonalVonNeumannGrid(
            (width, height), capacity=1, torus=True, random=self.random
        )

        model_reporters = {
            "Documented_count": WorkerStatus.DOCUMENTED.name,
            "Undocumented_count": WorkerStatus.UNDOCUMENTED.name,
            "Deported_count": WorkerStatus.DEPORTED.name,
        }

        agent_reporters = {
            "wage": lambda a: getattr(a, "wage", None),
        }

        self.datacollector = mesa.DataCollector(
            model_reporters=model_reporters, agent_reporters=agent_reporters
        )

        if ICE_density + worker_density > 1:
            raise ValueError("ICE deinsity + worker desnity must be less than 1")
        
        for cell in self.grid.all_cells:
            new_ICE_officer = ICE_officer(self, 1, 2)
            klass = self.random.choices(
                [new_ICE_officer, worker, None],
                com_weights=[worker_density, worker_density + ICE_density, 1],
            )[0]

            if klass == ICE_officer:
                ICE_officer = ICE_officer(self, vision=ICE_vision)
                ICE_officer.move_to(cell)
            elif klass == worker:
                worker = worker(
                    self,
                    wage_threshold = wage_threshold,
                    wage_constant = wage_constant,
                )
                worker.move_to(cell)

        self.running = True
        self._update_counts()
        self.datacollector.collect(self)

        print('agricultural model init')

    def step(self):

        self.agents.shuffle_do("step")
        self._udpate_counts()
        self.datacollector.collect(self)

        if self.steps > self.max_iters:
            self.running = False

        current_month = current_month + 1
        if current_month > 12:
            current_month = 1
            current_year += 1 
        print(current_year, current_month)

    def _update_counts(self):
        "helper functino for counting number of workers"
        counts = self.agents_by_type[worker].groupby("status").count()
    
        for Status in WorkerStatus: 
            setattr(self, status.name, counts.get(status, 0))