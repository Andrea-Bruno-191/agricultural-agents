import sys

from farm_worker_agent import (
    Worker, WorkerStatus, ICE_officer
    )
from farm_wage_utils import calc_wage
from farm_labor_model import agricultural_model
from mesa.visualization import (
    Slider,
    SolaraViz,
    SpaceRenderer,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle

# ICE_color = "#023098"
ICE_color = "red"
wage_color = "gold"

agent_colors = {
    WorkerStatus.DOCUMENTED: "#4C753B",
    WorkerStatus.UNDOCUMENTED: "#D18049",
    WorkerStatus.DEPORTED: "#110311"
}

def worker_or_officer_portrayal(agent):
    # print("agent:", agent, agent.unique_id, wage)
    if agent is None:
        return
    
    portrayal = AgentPortrayalStyle(size=200)

    if isinstance(agent, Worker):
        portrayal.update(("color", agent_colors[agent.status]))
    elif isinstance(agent, ICE_officer):
        portrayal.update(("color", ICE_color))
    
    # portrayal.update(("color", wage))

    return portrayal

def post_process(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.get_figure().set_size_inches(10, 10)

model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "height": 20,
    "width": 20,
    "worker_density": Slider("Initial Worker Density", 0.7, 0.1, 0.9, 0.1),
    "ICE_density": Slider("Initial ICE Density", 0.04, 0.0, 0.1, 0.01),
    "ICE_vision" : Slider("ICE Vison", 3, 1, 10, 1),
}

chart_component_workers = make_plot_component(
    {status.name.lower(): agent_colors[status] for status in WorkerStatus}
)
chart_component_wages = make_plot_component(
    {"wage": wage_color}
)


agricultural_model = agricultural_model()
renderer = SpaceRenderer(agricultural_model, backend="matplotlib")
renderer.draw_agents(worker_or_officer_portrayal)
renderer.post_process = post_process

page = SolaraViz(
    agricultural_model, 
    renderer,
    components=[chart_component_workers,
                chart_component_wages],
    model_params=model_params,
    name="Agricultural Agents in a Dynamic Model",
)
page # noqa
