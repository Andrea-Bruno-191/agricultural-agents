#! /usr/bin/env python3

"""
Some functions that implement how wages are set in a certain
season, geographical region, and worker availability.
"""


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
    wage = model.wage_baseline * get_employment_capacity(model.current_year, model.current_month) / (model.n_avail / 4) 
    return wage

def get_employment_capacity(year, month):
    return agri_month2work_needed[month]

#def calc_wage_threshold():
#    random.randint(1, 100)
#    return wage_threshold
    