#! /usr/bin/env python3

import math
from math import sqrt

global_state = {
    'n_jobs_total': 300,
    'farmer_wage_weekly': 750,
    # note that in the future we should model the immigration probability as
    # coming from the number of available jobs and possibly other model
    # parameters
    'immigration_prob_percent': 2, # chance chance of new worker/week
    'immigration_max_weekly': 5, # most workers/week who can come or go
}

# zipcode_list = ('96019', '96079', '96022', '96035')
zipcode_list = ['96001', '96002', '96003', '96006', '96007', '96008', '96009',
                '96010', '96011', '96013', '96014', '96015', '96016', '96017',
                '96019', '96020', '96021', '96022', '96023', '96024', '96025',
                '96027', '96028', '96029', '96031', '96032', '96033', '96034',
                '96035', '96037', '96038', '96039', '96040', '96041', '96044',
                '96046', '96047', '96048', '96049', '96050', '96051', '96052',
                '96054', '96055', '96056', '96057', '96058', '96059', '96061',
                '96062', '96063', '96064', '96065', '96067', '96068', '96069',
                '96070', '96071', '96073', '96074', '96075', '96076', '96078',
                '96079', '96080', '96084', '96085', '96086', '96087', '96088',
                '96089', '96090', '96091', '96092', '96093', '96094', '96095',
                '96096', '96097', '96099']

def make_zip2grid(zipcode_list):
    """A first stab at placing farmer zip codes on a grid.  I kludge it by
    putting a hard-coded list of coordinates; in the future I will cache the use
    of one of the Python geographic APIs, like openstreetmap's Nominatim.
    """
    zipcode2grid = {}
    # cheesy approach to picking rectangle size to fit this size
    nx, ny = n_cells2grid_size(len(zipcode_list))
    print(len(zipcode_list), sqrt(len(zipcode_list)), nx, ny, nx*ny)
    assert(nx * ny >= len(zipcode_list))
    for i, zipc in enumerate(zipcode_list):
        x = i % nx
        y = (i // nx) % ny
        print('xy:', x, y, x + y * nx)
        zipcode2grid[zipc] = (x, y)
    return zipcode2grid


def n_cells2grid_size(n_cells):
    """For now a really cheesy algorithm; there is some discussion here:
    https://math.stackexchange.com/questions/4581354/splitting-a-rectangle-into-mxn-pieces-with-target-aspect-ratio
    but I just take nx to be the square root + 2, and ny to be the square root
    """
    nx = math.floor(sqrt(len(zipcode_list))) + 2
    ny = math.floor(sqrt(len(zipcode_list)))
    return nx, ny


def load_chronology():
    """Scientist generates a chronology of events they want to inject into
    the simulation at various moments.  Example: a storm, a pandemic, a
    political veer, ..."""
    chron_fname = 'labor_chrono.txt'
    event_list = []
    with open(chron_fname, 'r') as f:
        for line in f.readlines():
            if line[0] == '#':
                continue
            date, evt_str = line.split(maxsplit=1)
            event_list.append((date, evt_str))
    print('after loading chrono:', event_list)
    return event_list
