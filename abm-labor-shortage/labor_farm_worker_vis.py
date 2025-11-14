#!/usr/bin/python3

# run with: solara run labor_farm_worker_vis.py

from mesa.visualization import SolaraViz, make_plot_component, make_space_component
from mesa.visualization.components import AgentPortrayalStyle

# change this to match your file name if it's not sir_model.py!
import labor_farm_worker as lfm
# from labor_deportation import *
# from labor_county import *

# The parameters we run the model with.
# Feel free to change these!
model_params = {'N_farm_workers':
                {'type': 'SliderInt',
                 'value': 60,
                 'min': 1,
                 'max': 90,
                 'step': 1
                 }}

def agent_portrayal(agent):
    # return AgentPortrayalStyle()
    # return AgentPortrayalStyle()
    radius = 0.2
    portrayal = {'marker': 's',
                 'color': 'blue',
                 'edgecolors': 'blue',
                 # 'filled': 'true',
                 # 'layer': 0,
                 'size': 2.75}
    if agent.info['documented']:
        portrayal['edgecolors'] = 'black'
    else:
        portrayal['edgecolors'] = 'red'
    if agent.info['employed']:
        portrayal['color'] = 'LimeGreen'
    # if agent.info['employed'] and agent.info['documented']:
    #     portrayal['color'] = 'LimeGreen'
    #     # portrayal['Layer'] = 1
    # if agent.info['employed'] and not agent.info['documented']:
    #     portrayal['color'] = '#ffd700'
    #     # portrayal['Layer'] = 1
    return portrayal

    # if isinstance(agent, lfm.FarmWorker):
    #     portrayal = {'Shape': 'circle',
    #                  'Color': 'brown',
    #                  'Filled': 'true',
    #                  'Layer': 0,
    #                  'r': radius}
    #     return portrayal
    # # default, if it was not one of those other cases
    # portrayal = {'Shape': 'circle',
    #              'Color': 'green',
    #              'Filled': 'false',
    #              'Layer': 0,
    #              'r': radius}
    # return portrayal
    
    # if not isinstance(agent, Farm):
    #     portrayal = {'Shape': 'circle',
    #                  'Color': 'brown',
    #                  'Filled': 'true',
    #                  'Layer': 0,
    #                  'r': radius}
    #     return portrayal
    # portrayal = {'Shape': 'circle',
    #              'Color': 'brown',
    #              'Filled': 'true',
    #              'Layer': 0,
    #              'r': radius}
    # radius = (agent.size_m2 / 162.0) * 0.9
    # portrayal = {'Shape': 'circle',
    #              'Color': 'brown',
    #              'Filled': 'true',
    #              'Layer': 0,
    #              'r': radius}
    # if agent.owner_id == -1:
    #     portrayal['color'] = 'red'
    #     portrayal['filled'] = False
    # else:
    #     farm_agent = 24.2       # FIXME: just to get it to run for now
    #     portrayal['filled'] = True
    #     if farm_agent >= 30:
    #         portrayal['color'] = 'blue'
    #     else:
    #         portrayal['color'] = 'green'
    # return portrayal

farm_worker_model = lfm.FarmWorkerModel(model_params['N_farm_workers']['value'])
SpaceGraph = make_space_component(agent_portrayal)
FarmWorkerPlot = make_plot_component(('Workers', 'Employed', 'Documented'))
# FarmWorkerPlot = make_plot_component('Workers')

page = SolaraViz(farm_worker_model,
                 components=[SpaceGraph, FarmWorkerPlot],
                 # components=[FarmWorkerPlot],
                 model_params=model_params,
                 name='Simple farm worker visualization')
