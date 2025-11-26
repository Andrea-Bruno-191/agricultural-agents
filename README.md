# agent based model for farm workers and ICE deportations

## Running

If you have *already* done the initial python setup then you can
simply run these instructions:

```sh
source abm-mesa-venv/bin/activate
solara run farm_labor_app.py
```

(Otherwise look below at the section `<Set up your python packages,
mostly mesa and solara`.)


## Purpose and scope

Meant to model how ICE aggression impacts wages and the cost of
labor in the agricultural labor market. 


## Agent design

Workers are either documented or undocumented. Undocumented workers
are willing to work for less, but will expect higher pay to stay
in the United States as their fear of being detained grows. 

Wage is calculated depending on the amount of work needed and
the number of agents in the model. Workers have a reservation wage
which is defined by their documentation status and how aggressive
ICE is. 

## Set up your python packages, mostly mesa and solara

Using the Mesa framework we define various classes.  Start by
installing needed python s/w:
```sh
sudo apt install python3-venv
python3 -m venv abm-mesa-venv/
source abm-mesa-venv/bin/activate
pip3 install mesa solara altair
pip3 install networkx matplotlib
```

## Running and visualizing the model

For now the model that is somewhat complete is `farm_worker_agent.py`
and you can run its visualization with:

```sh
solara run farm_labor_app.py
```

NOTE: The model is yet to implement data regarding wage dynamics
in the agricultural sector. "Work Needed" per month is based on data
from the BLS regarding seasonal employment in the farm sector.  

## the files that implement the models


`farm_labor_model.py`
: Farm - where the agents interact. 

`farm_wage_utils.py`
:Calculates the external wage based on seasonal demand and the
wage baseline. 

`farm_worker_agent.py`
: Tracks individual laborers and defines their behavior.

`farm_labor_app.py`
: visualization for the overall labor county system
: run it with ``solar run farm_labor_app.py``
