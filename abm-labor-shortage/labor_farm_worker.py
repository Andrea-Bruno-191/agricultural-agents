#!/usr/bin/python3

import random
import math
import sys
from scipy.special import expit # a sigmoid function

from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from labor_farm import Farm
from labor_utils import zipcode_list, make_zip2grid, n_cells2grid_size
import labor_utils as utils

worker_info_fields = ('residence', 'employed', 'documented', 'salary',
                      'productivity', 'assets')
zip2grid = make_zip2grid(zipcode_list)

def main():
    """in this context (using mesa) the main() function is really just for
    demonstrating the model and agent code."""
    m = FarmWorkerModel(60, 1234) # force a seed of 1234
    for i in range(24):
        m.step()

class FarmWorker(Agent):
    def __init__(self, model, residence, employed, documented, salary,
                 productivity):
        super().__init__(model)
        assert(isinstance(residence, str))
        assert(isinstance(documented, bool))
        self.info = dict.fromkeys(worker_info_fields, None)
        self.info['residence'] = residence # where do we live?
        self.info['employed'] = employed
        self.info['documented'] = documented
        # hourly salary in dollars
        self.info['salary'] = 35
        # labor output/hour
        self.info['productivity'] = productivity
        # starting assets in dollars
        self.info['assets'] = 0

    def do_relocate(self):
        """At every step a farm worker has a certain probability of relocating
        to another zip code."""
        if random.random() < 0.001: # rare move, but for now make it 0.1%
            new_zip = random.choice(zipcode_list)
            if new_zip != self.info['residence']: # is it a move?
                old_xy = zip2grid[self.info['residence']]
                new_xy = zip2grid[new_zip]
                # print(f'relocate agent_{self.unique_id} from'
                #       + f' {self.info["residence"]} ({old_xy}) to {new_zip}'
                #       + f' ({new_xy})')
                self.residence = new_zip
                self.model.grid.move_agent(self, new_xy)

    def do_job_update(self, **kwargs):
        """At every step a farm worker might find or lose a job.  This will
        depend in part on external conditions.  For now chesse it with simple
        toss of the dice.
        """
        # print(f'====== JOB_UPDATE_{self.model.steps}_{self.unique_id}_kwargs:'
        #       + f' {kwargs} =====')
        # for k, val in kwargs.items():
        #     print('ARG:', k, val)
        n_jobs_offered = kwargs['n_jobs_offered']
        n_unemployed = kwargs['n_unemployed']
        if kwargs['n_unemployed'] == 0 or kwargs['n_total_workers'] == 0:
            # print('  NO_JOB_UPDATE')
            return
        # if you don't have a job, then see if you get one
        if not self.info['employed'] and kwargs['n_jobs_offered'] > 0:
            prob_job_offered = kwargs['n_jobs_offered'] / kwargs['n_unemployed']
            if random.random() < prob_job_offered:
                self.info['employed'] = True
                print('NEW_JOB:', self.unique_id, self.info)
        # if you have a job, then see if you lose it
        if self.info['employed'] and kwargs['n_jobs_offered'] < 0:
            prob_job_lost = kwargs['n_jobs_offered'] / kwargs['n_total_workers']
            random_throw = random.random()
            if random_throw < abs(prob_job_lost):
                self.info['employed'] = False
                print('LOSE_JOB:', self.unique_id, self.info)
                print('         ', random_throw, kwargs['n_jobs_offered'],
                      prob_job_lost)
        
        # if self.info['employed']:
        #     if random.random() < 0.01:
        #         self.info['employed'] = False # lose the job
        # else:
        #     if random.random() < 0.012:
        #         self.info['employed'] = True # find a job

    def get_coords(self):
        """Return the (x, y) grid coordinates that correspond to this agent's
        residence zip code."""
        xy = zip2grid[self.info['residence']]
        return xy

    def step(self):
        """Not much to do now.  It used to be that this step() method would
        kick off all agent updates, but now the new mesa architecture allows
        the model step() to call other agent methods, so eventually there will
        not be much here.  For example, do_job_update() is now called
        independently, and eventually I might also call do_relocate()
        independently.  (But for now I call do_relocate() here.)"""
        self.do_relocate()

class FarmWorkerModel(Model):
    """This is a trivial model used to examine/debug/visualize a single farm
    worker, or a few.  There is no labor context."""
    def __init__(self, N_farm_workers, seed=None):
        super().__init__(seed=seed)
        self.num_agents = N_farm_workers
        width, height = n_cells2grid_size(len(zipcode_list))
        self.grid = MultiGrid(width, height, torus=True)
        self.running = True
        self.datacollector = DataCollector(
            model_reporters = {'Workers': get_total_workers,
                               'Employed': get_total_employed,
                               'Documented': get_total_documented
                               })
        # set up info that does not come initialization, i.e. specific to this
        # model.  example is handling age and loading the table of exogenous
        # events
        self.age_weeks = 0
        self.event_list = utils.load_chronology()
        # at the start we need to give all the workers we create a
        # job, if there are jobs available, so we have a couple of
        # variables to keep track of that
        initial_n_jobs = utils.global_state['n_jobs_total']
        initial_remaining_jobs = initial_n_jobs
        # create agents
        for i in range(self.num_agents):
            zipcode = random.choice(zipcode_list)
            employed = True if initial_remaining_jobs > 0 else False
            if employed:
                initial_remaining_jobs -= 1
            documented = True if random.random() < 0.7 else False
            farmer = FarmWorker(self, zipcode, employed, documented, 0, 10)
            print(f'INIT_FARMER: {farmer.info}')
            # self.agents.add(farmer)
            self.grid.place_agent(farmer, farmer.get_coords())
            print(f'#NEW_FARMER: {farmer.unique_id} {farmer.get_coords()}')
        print('GET_STUFF_AFTER_INIT:', get_total_workers(self),
              get_total_employed(self), get_total_documented(self))
    def step(self):
        """For the farm worker model the steps involve running the 'step' method
        for each agent, and then handling external events from the chronology,
        and then calling the boiler plate datacollector events which allow the
        plotting mechanism to do its thing.

        """
        # first simple updating of the model and calling each worker's step
        self.age_weeks += 1
        assert(self.age_weeks == self.steps) # self.steps is maintained by mesa
        self.agents.shuffle_do('step')
        # self.agents.do('do_job_update', utils.global_state)
        # now some calculations to update the state machine of what jobs are
        n_total_workers = get_total_workers(self)
        n_employed = get_total_employed(self)
        # n_jobs_offered could be positive or negative
        n_jobs_total = utils.global_state['n_jobs_total']
        n_jobs_offered = n_jobs_total - n_employed
        n_unemployed = n_total_workers - n_employed
        print(f'================= week {self.steps} =================')
        print('n_total_workers', n_total_workers)
        print('n_employed', n_employed)
        print('n_jobs_offered', n_jobs_offered)
        print('n_unemployed', n_unemployed)
        self.agents.do('do_job_update', n_jobs_offered=n_jobs_offered,
                       n_unemployed=n_unemployed, n_total_workers=n_total_workers)
        # self.agents.do('do_relocate')
        self.handle_chrono_events()
        self.handle_immigration(n_employed, n_jobs_offered, n_total_workers,
                                n_unemployed)
        self.datacollector.collect(self)

    def handle_chrono_events(self):
        """See if any event in our "endogenous chronology" needs handling, and
        if so do it."""
        for evt in self.event_list:
            if int(evt[0]) == self.age_weeks:
                print('APPLY_EVENT:', evt)
                self.apply_event(evt[1])

    def apply_event(self, evt_body):
        """Handle an endogenous event - this updates the simulation state
        based on things that happen."""
        evt_parsed = evt_body.strip().split(',')
        if evt_parsed[0] == 'ICE_RAID':
            print('ICE_RAID:', evt_parsed, 'removing workers')
            # first make a list of removals, then do the removals
            n_to_remove = int(evt_parsed[1])
            n_marked_for_removal = 0
            removal_list = []
            for agent in self.agents:
                if not agent.info['documented']:
                    # agent.remove()
                    removal_list.append(agent)
                    n_marked_for_removal += 1
                    if n_marked_for_removal >= n_to_remove:
                        break
            for agent in removal_list:
                print('REMOVE:', agent.unique_id, agent.info)
                agent.remove()
        elif evt_parsed[0] == 'SET':
            param = evt_parsed[1].strip()
            val = evt_parsed[2].strip()
            utils.global_state[param] = float(val)
            print('NEW_GLOBAL_STATE:', utils.global_state)
        elif evt_parsed[0] == 'INCREMENT':
            param = evt_parsed[1].strip()
            val = evt_parsed[2].strip()
            utils.global_state[param] += float(val)
            print('NEW_GLOBAL_STATE:', utils.global_state)
            
    def handle_immigration(self, n_employed, n_jobs_offered,
                           n_total_workers, n_unemployed):
        """Immigration can probably be simulated in a sophisticated
        manner.  For now I just do it as a probability of people
        moving in or out based on the job situation.

        """
        # # make sure that the "jobs offered" and "unemployed" numbers
        # # are consistent - or wait, maybe we should let them be
        # # inconsistent since things will shake out correctly after a
        # # few weeks
        # assert(not (n_jobs_offered > 0) and (n_unemployed > 0))
        n_people_move_in = round(utils.global_state['immigration_max_weekly']
                                 * (2*expit(0.1*n_jobs_offered)))
        n_people_move_out = round(utils.global_state['immigration_max_weekly']
                                  * (2*expit(0.1*n_unemployed)))
        print('handle_immigration:', n_employed, n_jobs_offered,
              n_total_workers, n_unemployed,
              ' -- ', n_people_move_in, n_people_move_out)
        if n_people_move_in > 0:
            for i in range(n_people_move_in):
                zipcode = random.choice(zipcode_list)
                employed = False # start without a job
                documented = True if random.random() < 0.7 else False
                farmer = FarmWorker(self, zipcode, employed, documented, 0, 10)
                self.grid.place_agent(farmer, farmer.get_coords())
                print('NEW_AGENT:', farmer.unique_id, farmer.info)
        if n_people_move_out > 0:
            for i in range(n_people_move_out):
                # remove a random agent
                a = random.choice(self.agents)
                print('REMOVE_AGENT:', a.unique_id, a.info)
                a.remove()
        print(f'GET_STUFF_AFTER_IMMIGRATION_{self.steps}:'
              + f' tot: {get_total_workers(self)} - employed:'
              + f' {get_total_employed(self)} docu: {get_total_documented(self)}')
                


## below we have utility functions for this model and agent

def get_total_workers(model):
    # NOTE: here I could just return len(model.agents), but we might have
    # different types of workers in the future, so keep it flexible
    n = 0
    for agent in model.agents:
        if isinstance(agent, FarmWorker):
            n += 1
    return n

def get_total_employed(model):
    n = 0
    for agent in model.agents:
        if isinstance(agent, FarmWorker) and agent.info['employed']:
            n += 1
    return n

def get_total_documented(model):
    n = 0
    for agent in model.agents:
        if isinstance(agent, FarmWorker) and agent.info['documented']:
            n += 1
    return n

# some simple demonstrating/testing
if __name__ == '__main__':
    print('RUNNING_main')
    main()
