#!/usr/bin/python3

import math
import numpy as np
import mesa
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.experimental.continuous_space import ContinuousSpaceAgent

from worker_agent import current_month, current_year, WorkerStatus, Worker, ICE_officer
from farm_wage_utils import work_needed, wage_baseline

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

        self.n_avail = round(width*height*worker_density)
        self.grid = mesa.discrete_space.OrthogonalVonNeumannGrid(
            (width, height), capacity=1, torus=True, random=self.random
        )

        model_reporters = {
            "documented": WorkerStatus.DOCUMENTED.name,
            "undocumented": WorkerStatus.UNDOCUMENTED.name,
            "deported": WorkerStatus.DEPORTED.name,
        }

        agent_reporters = {
            "wage": lambda a: getattr(a, "wage", None),
        }

        self.datacollector = mesa.DataCollector(
            model_reporters=model_reporters, agent_reporters=agent_reporters
        )

        if ICE_density + worker_density > 1:
            raise ValueError("ICE density + worker density must be less than 1")

        for cell in self.grid.all_cells:
            print(f"model_init_iterate_cell: {cell}")
            # new_ICE_officer = worker_agent_andrea.ICE_officer(self, 1, 2)
            # new_worker = Worker(self, 3, 17, 15)
            klass = self.random.choices(
                [ICE_officer, Worker, None],
                cum_weights=[worker_density, worker_density + ICE_density, 1],
            )[0]
            print('this_klass:', klass)

            if klass == ICE_officer:
                new_ICE_officer = ICE_officer(self, 1, 2)
                new_ICE_officer = worker_agent.ICE_officer(self, vision=ICE_vision)
                new_ICE_officer.move_to(cell)
            elif klass == Worker:
                new_worker = Worker(self, 3, 17, 15)
                # new_worker = Worker(
                #     self,
                #     wage_threshold = wage_threshold,
                #     wage_constant = wage_constant,
                # )
                new_worker.move_to(cell)

        self.running = True
        self._update_counts()
        print("====================================================")
        print(self.datacollector)
        self.datacollector.collect(self)

        print('agricultural model init')

    def step(self):
        print("MODEL: step")
        self.agents.shuffle_do("step")
        self._update_counts()
        self.datacollector.collect(self)

        if self.steps > self.max_iters:
            self.running = False

        current_month = current_month + 1
        if current_month > 12:
            current_month = 1
            current_year += 1
        print(current_year, current_month)

    def _update_counts(self):
        """helper function for counting number of workers"""
        print('--> bytype:', self.agents_by_type[Worker])
        print('--> bytype:', dir(self.agents_by_type[Worker]))
        counts = self.agents_by_type[Worker].groupby("status").count()
        for status in WorkerStatus:
            setattr(self, status.name, counts.get(status, 0))
