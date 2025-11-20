# agent based model for labor shortage

## Running

If you have *already* done the initial python setup then you can
simply run these instructions:

```sh
source labor-shortage-venv/bin/activate
solara run labor_farm_worker_vis.py
```

(Otherwise look below at the section `<Set up your python packages,
mostly mesa and solara`.)


## Purpose and scope

First stab at defining agents for labor effects in a geographical area
due to any of these factors:

* Mass deportation
* Large scale strikes

Other factors that could be interesting but we are not looking at now:

* Large scale military draft
* Epidemics

## Agent design

One can think of agents and "reservoirs".

Agents have state for several individual instances, like a person, an
institutional office, a business location (farm or factory).  They are
sensitive to coming "close" to another agent and can interact.  The
closeness can be geographical, or it could be a "network" closeness.

Reservoirs have global state, like economic indicators or other
parameters that we do not model as interacting individuals.

## Set up your python packages, mostly mesa and solara

Using the Mesa framework we define various classes.  Start by
installing needed python s/w:
```sh
sudo apt install python3-venv
python3 -m venv labor-shortage-venv/
source labor-shortage-venv/bin/activate
pip3 install mesa solara altair
pip3 install networkx matplotlib
```

## Running and visualizing the model

For now the model that is somewhat complete is `labor_farm_worker.py`
and you can run its visualization with:

```sh
solara run labor_farm_worker_vis.py
```

NOTE: so far (2025-11-14) the labor_farm_worker model and visualization
are all that is operational, but they make for an interesting model.
Below are some notes on parts that are not yet fleshed out.

## the files that implement the models

`labor_county.py` - CountyModel

labor_deportation.py

`labor_farm.py`
: Farm - a collection of fields, each field representing a grid
  location

`labor_farm_worker.py`
: Track individual laborers

`labor_county_vis.py`
: visualization for the overall labor county system
: run it with ``solar run labor_county_vis.py``
