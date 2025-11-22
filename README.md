# agent based model for farm workers and ICE deportations

## Running

If you have *already* done the initial python setup then you can
simply run these instructions:

```sh
source farm-labor-venv/bin/activate
solara run farm_labor_app.py
```

(Otherwise look below at the section `<Set up your python packages,
mostly mesa and solara`.)


## Purpose and scope

First stab at defining agents for labor effects in a geographical area
due to any of these factors:

* Mass deportation
* Large scale strikes


## Agent design

Agents respond to wages, which are set by the firm according to
the amount of labor needed and the number of workers available to
complete this work. 

Reservoirs have global state, like economic indicators or other
parameters that we do not model as interacting individuals.

## Set up your python packages, mostly mesa and solara

Using the Mesa framework we define various classes.  Start by
installing needed python s/w:
```sh
sudo apt install python3-venv
python3 -m venv farm-labor-venv/
source farm-labor-venv/bin/activate
pip3 install mesa solara altair
pip3 install networkx matplotlib
```

## Running and visualizing the model

For now the model that is somewhat complete is `farm_worker_agent.py`
and you can run its visualization with:

```sh
solara run farm_labor_app.py
```

NOTE: so far (2025-11-14) the labor_farm_worker model and visualization
are all that is operational, but they make for an interesting model.
Below are some notes on parts that are not yet fleshed out.

## the files that implement the models


`labor_farm.py`
: Farm - a collection of fields, each field representing a grid
  location

`labor_farm_worker.py`
: Track individual laborers

`labor_county_vis.py`
: visualization for the overall labor county system
: run it with ``solar run labor_county_vis.py``
