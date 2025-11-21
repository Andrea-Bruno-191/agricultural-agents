#!/usr/bin/python3

import math
import numpy as np
import random
import mesa
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.experimental.continuous_space import ContinuousSpaceAgent

from farm_worker_agent import WorkerStatus, Worker, ICE_officer
from farm_wage_utils import calc_wage, wage_baseline

class agricultural_model(Model):
    def __init__(
        self,
        width = 20,
        height = 20,
        worker_density = 0.7,
        ICE_density = 0.05,
        ICE_vision = 3,
        movement=True,
        seed=None,
        max_iters=100
    ):
        super().__init__(seed=seed)
        # current month is the global date, all agents are put in 
        self.current_month = 1
        self.current_year = 2022
        self.movement = movement
        self.max_iters = max_iters
        # n_avail is the number of people available to do work
        self.n_avail = round(width*height*worker_density)
        self.wage_baseline = wage_baseline
        # self.wage = calc_wage(self.current_year,
        #                       self.current_month, '96099',
        #                       self.n_avail, self.wage_baseline)
        self.wage = calc_wage(self)
        self.grid = mesa.discrete_space.OrthogonalVonNeumannGrid(
            (width, height), capacity=1, torus=True, random=self.random
        )

        model_reporters = {
            "documented": WorkerStatus.DOCUMENTED.name,
            "undocumented": WorkerStatus.UNDOCUMENTED.name,
            "deported": WorkerStatus.DEPORTED.name,
            # "wage": WorkerStatus.WAGE.name,
            "wage": calc_wage,
        }

        agent_reporters = {
        }

        self.datacollector = mesa.DataCollector(
            model_reporters=model_reporters, agent_reporters=agent_reporters
        )

        if ICE_density + worker_density > 1:
            raise ValueError("ICE density + worker density must be less than 1")

        for cell in self.grid.all_cells:
            print(f"model_init_iterate_cell: {cell}")
            # new_ICE_officer = farm_worker_agent.ICE_officer(self, 1, 2)
            # new_worker = Worker(self, 3, 17, 15)
            klass = self.random.choices(
                [ICE_officer, Worker, None],
                cum_weights=[ICE_density, worker_density + ICE_density, 1],
            )[0]
            print('this_klass:', klass)

            if klass == ICE_officer:
                new_ICE_officer = ICE_officer(self, 1, 2)
                #new_ICE_officer = farm_worker_agent.ICE_officer(self, vision=ICE_vision)
                new_ICE_officer.move_to(cell)
            elif klass == Worker:
                new_worker = Worker(self, 3, 15, random.randint(0, 100))
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

        self.current_month = self.current_month + 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        print(self.current_year, self.current_month)

    def _update_counts(self):
        """helper function for counting number of workers"""
        print('--> bytype:', self.agents_by_type[Worker])
        print('--> bytype:', dir(self.agents_by_type[Worker]))
        counts = self.agents_by_type[Worker].groupby("status").count()
        for status in WorkerStatus:
            setattr(self, status.name, counts.get(status, 0))
