#!/usr/bin/python3

# run with: solara run labor_county_vis.py

from mesa.visualization import SolaraViz, make_plot_component, make_space_component

# change this to match your file name if it's not sir_model.py!
from labor_farm import *
from labor_farm_worker import *
from labor_deportation import *
from labor_county import *

# The parameters we run the model with.
# Feel free to change these!
model_params = {'N_fields': 200,
                'N_dwellers': 188,
                'width': 40,
                'height': 30}

def agent_portrayal(agent):
    radius = 0.2
    if not isinstance(agent, Farm):
        portrayal = {'Shape': 'circle',
                     'Color': 'brown',
                     'Filled': 'true',
                     'Layer': 0,
                     'r': radius}
        return portrayal
    portrayal = {'Shape': 'circle',
                 'Color': 'brown',
                 'Filled': 'true',
                 'Layer': 0,
                 'r': radius}
    radius = (agent.size_m2 / 162.0) * 0.9
    portrayal = {'Shape': 'circle',
                 'Color': 'brown',
                 'Filled': 'true',
                 'Layer': 0,
                 'r': radius}
    if agent.owner_id == -1:
        portrayal['color'] = 'red'
        portrayal['filled'] = False
    else:
        farm_agent = 24.2       # FIXME: just to get it to run for now
        portrayal['filled'] = True
        if farm_agent >= 30:
            portrayal['color'] = 'blue'
        else:
            portrayal['color'] = 'green'
    return portrayal

county_model = CountyModel(model_params['N_fields'],
                           model_params['N_dwellers'],
                           model_params['width'],
                           model_params['height'])
SpaceGraph = make_space_component(agent_portrayal)
CountyPlot = make_plot_component(('W', 'E', 'D'))

page = SolaraViz(county_model,
                 model_params=model_params,
                 components=[SpaceGraph, CountyPlot],
                 name='Simple labor visualization')
