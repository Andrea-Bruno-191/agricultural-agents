#! /usr/bin/env python3

"""
Some functions that implement how wages are set in a certain
season, geographical region, and worker availability.
"""


agri_month2work_needed = {1: 27, 2: 33, 3: 33, 4: 33, 5: 33, 6: 33, 7: 33, 8: 33,
                          9: 33, 10: 40, 11: 41, 12: 33}
wage_baseline = 17

def calc_wage(year, month, zip_code, n_workers_avail, wage_baseline, work_needed):
    """Simplified model of wage, uses the agri_month2work_needed table."""
    work_needed = agri_month2work_needed[month]
    wage = wage_baseline * work_needed / n_workers_avail 
    """how many workers we have? should change the work_needed table to be close ##to number of worker agents typically in model"""
    return wage

