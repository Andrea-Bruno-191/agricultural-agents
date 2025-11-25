#! /usr/bin/env python3

"""
Some functions that implement how wages are set in a certain
season, geographical region, and worker availability.
"""
import random

agri_month2work_needed = {1: 35, 2: 35, 3: 34, 4: 42, 5: 47, 6: 47, 7: 44, 8: 45,
                          9: 44, 10: 43, 11: 39, 12: 35}
wage_baseline = 17

# def get_current_wage(model):
#     return calc_wage(model.year, model.month, '96099', model.n_avail,
#                      model.wage_baseline)

# def calc_wage(year, month, zip_code, n_workers_avail, wage_baseline):
def calc_wage(model):
    """Simplified model of wage, uses the agri_month2work_needed table."""
    # work_needed = agri_month2work_needed[month]
    wage = model.wage_baseline * get_employment_capacity(model.current_year, model.current_month) / (0.2 * model.n_avail) 
    return wage

def get_employment_capacity(year, month):
    """The baseline for employment capacity comes from seasonal
    cyclical set of values in agri_month2work_needed. On top of that we add
    a stochastic component that will add or subtract up to 5% of the workers
    needed to sustain agricultural activity.  
    """
    baseline = agri_month2work_needed[month]
    deviation = 0.05 * baseline * 2*(random.random() - 1)
    return baseline + deviation

#def calc_wage_threshold():
#    random.randint(1, 100)
#    return wage_threshold ok 
    