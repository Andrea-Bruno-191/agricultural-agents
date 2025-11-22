"""
Agricultural labor model - mesa app file. 
This has the top level layout of graphical components for the
agricultural model, using a solara framework. 
This is a based the "Civil Unrest" model offered by
the mesa development team: 

https://mesa.readthedocs.io/latest/examples/advanced/epstein_civil_violence.html

To run this visualization as we describe in the README.md file,
you can type: 

solara run farm_labor_app.py
"""

import sys



from mesa.visualization import (
    Slider,
    SolaraViz,
    SpaceRenderer,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle


# the app component needs some classes and functions from the model
#and the agent, so we import them here. 
from farm_worker_agent import (
    Worker, WorkerStatus, ICE_Officer
)
from farm_wage_utils import calc_wage
from farm_labor_model import AgriculturalModel

ICE_color = "#DD5A4C"
wage_color = "gold"


#these are the colors for the agents in the grid. Make sure 
#these match the WorkerStatus type defined in farm_worker_agent.py

agent_colors = {
    WorkerStatus.DOCUMENTED: "#4C753B", #greenish
    WorkerStatus.UNDOCUMENTED: "#D18049", #orangeish
    WorkerStatus.DEPORTED: "#110311" #black 
}

def worker_or_officer_portrayal(agent):
    """In Mesa, this function is used to draw the agent in the spacial
    grid. For now we keep the basic disc shape and mostly the size and color.
    We use a single function that checks if the agent is one type or another, 
    and colors it accordingly. 
    """
    if agent is None:
        return
    
    portrayal = AgentPortrayalStyle(size=200)

    if isinstance(agent, Worker):
        portrayal.update(("color", agent_colors[agent.status]))
    elif isinstance(agent, ICE_Officer):
        portrayal.update(("color", ICE_color))

    return portrayal

"""Post_process is a hook that gets called at the end of the graphical 
processing.
"""

def post_process(ax):
    """Set the character of the window that shows the agents in a
    spacial grid. No tick-marks, 10x10 inches. 
    """
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.get_figure().set_size_inches(10, 10)

# model_params is used to set up the sliders in the graphical interface,
# which allows users to manipulate the scenario parameters. 
# Note that at this time, these are redundant to the AgriculturalModel's
# __init__ method. 
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "height": 20,
    "width": 20,
    "worker_density": Slider("Initial Worker Density", 0.4, 0.1, 0.9, 0.1),
    "ICE_density": Slider("Initial ICE Density", 0.02, 0.0, 0.1, 0.01),
    "ICE_agent_vision" : Slider("ICE Aggression", 3, 1, 10, 1),
}

#These are ticker style plots of quantities which are calculated in
#the model. We have one plot that shows the number of workers with
#each status, and another which shows the wage calculated by the model. 
# The two objects we make here will be passed to the SolaraViz() call
#below, which sets up the graphical interface. 
chart_component_workers = make_plot_component(
    {status.name.lower(): agent_colors[status] for status in WorkerStatus}
)
chart_component_wages = make_plot_component(
    {"wage": wage_color}
)

#Great, we're almost done! Now we just create the model object 
#and then make the graphical portions. 
agricultural_model = AgriculturalModel()
renderer = SpaceRenderer(agricultural_model, backend="matplotlib")
renderer.draw_agents(worker_or_officer_portrayal)
renderer.post_process = post_process

#This call is paradigmatic in Solara, and sets up the graphical interface
#In the web browser. 
page = SolaraViz(
    agricultural_model, 
    renderer,
    components=[chart_component_workers,
                chart_component_wages],
    model_params=model_params,
    name="Agricultural Agents in a Dynamic Model",
)
