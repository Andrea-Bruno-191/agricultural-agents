#!/usr/bin/python3

"""Agricultural labor model - mesa model file. 
This file defines the model, which in the mesa framework: 
-Coordinates all of the agents
-Puts them on a spacial grid 
-Manages time steps
-Tracks some global quantities. 
"""

import math
import numpy as np
import random
import mesa
from scipy.special import expit

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.experimental.continuous_space import ContinuousSpaceAgent

# The model will use some classes and functions from the agent file and
# from our utility file, so we import those here. 
from farm_worker_agent import WorkerStatus, Worker, ICE_Officer
from farm_wage_utils import calc_wage, wage_baseline

class AgriculturalModel(Model):
    """
    The model is derived from Mesa's model base class and adds to it:
    -Tracking a spacial grid on which the workers and ice agents interact.
    -Tracks the month and the year, as well as farm labor needed accordingly.
    -Tracks all worker agents: where they are and their status. 
    """
    def __init__(
        self,
        width = 20, height = 20,
        worker_density = 0.4, ICE_density = 0.02,
        ICE_agent_vision = 3,
        #ICE agent vision is a simulacrum for how aggressive immigration
        #policy is. This defines how they move. 
        movement=True, seed=None,
        max_iters=100
    ):
        """
        Initialize the model! This starts by calling the base class
        initialization function, then it stores the variables we gave it,
        then it creates the grid. 
        """
        super().__init__(seed=seed)
        # current month is the global date, all agents are put in 
        self.current_month = 1
        self.current_year = 2022
        self.movement = movement
        self.max_iters = max_iters
        # n_avail is the number of people available to do work
        self.n_avail = round(width*height*worker_density)
        self.wage_baseline = wage_baseline
        self.deport_history = []
        # self.wage = calc_wage(self.current_year,
        #                       self.current_month, '96099',
        #                       self.n_avail, self.wage_baseline)
        self.wage = calc_wage(self)
        self.grid = mesa.discrete_space.OrthogonalVonNeumannGrid(
            (width, height), capacity=1, torus=True, random=self.random
        )

        #Now we need to set a few things up to let mesa's graphics system
        #get information for plots and spacial agent portrayal. 
        #The overall dictionairy for this is #model_reporters, which we set
        #here, and which we will then pass to mesa.DataCollector(). 
        model_reporters = {
            "documented": WorkerStatus.DOCUMENTED.name,
            "undocumented": WorkerStatus.UNDOCUMENTED.name,
            "deported": WorkerStatus.DEPORTED.name,
            "documented_leaving": WorkerStatus.DOCUMENTED_LEAVING.name,
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
            klass = self.random.choices( #randomly chooses between worker and
                #ICE agents. 
                [ICE_Officer, Worker, None],
                cum_weights=[ICE_density, worker_density + ICE_density, 1],
            )[0]
            #Create agent objects and put them in cells according
            #to the density. 
            print('this_klass:', klass)
            if klass == ICE_Officer:
                new_ICE_Officer = ICE_Officer(self, ICE_agent_vision)
                new_ICE_Officer.move_to(cell)
            elif klass == Worker:
                new_worker = Worker(self)
                new_worker.move_to(cell)

        #We're done with setup, let's kick it off! 
        #There are three steps: 
        # Tell the model we're operational by telling
        # the model to start running, start up the graphical
        # stuff. 
        self.running = True
        self._update_counts()
        self.datacollector.collect(self)

    def step(self):
        """Standard mesa step function: 
        A) call each agen'ts step() method,
        B) update graphics
        C) update timeline. 
        """
        print("MODEL: step")
        self.agents.shuffle_do("step")
        self.handle_removals()
        self.handle_immigration()
        self._update_counts()
        self.datacollector.collect(self)
        self.wage = calc_wage(self) 

        self.current_month = self.current_month + 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1

        #Stops us from running forever. 
        if self.steps > self.max_iters:
            self.running = False

    def _update_counts(self):
        """helper function for counting number of workers in the three
        possible states defined in WorkerStatus: DOCUMENTED, UNDOCUMENTED,
        DEPORTED
        """
        counts = self.agents_by_type[Worker].groupby("status").count()
        if not WorkerStatus.DEPORTED in counts: 
            counts[WorkerStatus.DEPORTED] = 0
        for status in WorkerStatus:
            setattr(self, status.name, counts.get(status, 0))
        #Update the history of how many workers got deported each month in the
        #last 12 months. 
        self.deport_history.append(counts[WorkerStatus.DEPORTED])
        if len(self.deport_history) > 12: 
            del self.deport_history[0]
        if len(self.deport_history) == 0: 
            self.deport_monthly_average = 0
        else: 
            self.deport_monthly_average = sum(self.deport_history) / len(self.deport_history)


    def handle_removals(self):
        """Helper function which removes agents with the 'deported' status
        from the model."""
        removal_list = []
        deportation_list = []
        for a in self.agents: 

            #first prepare the list to be deported
            if isinstance(a, Worker) and (a.status == WorkerStatus.DEPORTED 
                                        or a.status == WorkerStatus.DOCUMENTED_LEAVING):
                #print('REMOVE_WORKER_AGENT:', a.unique_id)
                deportation_list.append(a)
        for a in deportation_list: 
            a.remove()
            print("Just_removed_agent:", a.unique_id, a.status, "remaining:",
                  len(self.agents))
        self.n_avail = len(self.agents)

    def handle_immigration(self):
        """This method introduces new worker agents into our community, 
        based on the current wage being offered."""
        monthly_cap = 10 #not yet sophisticated
        mobility_factor = .05
        sigmoid_arg = (self.wage - wage_baseline) * mobility_factor 
        incoming_prob = expit(sigmoid_arg)
        n_incoming = round(monthly_cap * incoming_prob)
        print("IMMIGRATION: prob, incoming:", incoming_prob, n_incoming)
        for i in range(n_incoming):
            new_worker = Worker(self)
            new_worker.move_to(self.grid.empties.cells[0])
            print("NEW_WORKER:", new_worker.unique_id, new_worker.pos)
            #assert(self.grid.exists_empty_cells())
            #cell = self.grid.select_cells(only_empty = True)[0]
            #self.grid.place_agent(worker)


