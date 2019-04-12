# data-sharing-abm-demo
Interactive front-end demo of the [data-sharing-abm-model](https://github.com/theodi/data-sharing-abm-model).

## How to run the app

Using conda environments:

* Navigate to the `final-app` folder in the terminal
* In a terminal, activate the correct environment: `conda activate odi-app`
* Start the app: `python odi-app.py`
* In what follows as output, you will see a message along the lines of `Running on http://0.0.0.0:8050/``
* Navigate to `http://127.0.0.1:8050/` in your browser and you should see the app  (_not_ the address you see in your terminal).

You can also run the app using docker if you have it installed on your computer:

* Navigate into the `final-app` folder in the terminal
* Type `make run`
* Go to `http://127.0.0.1:8050/` in your browser (_not_ the address you see in your terminal)

## Relevant files for the app

* `odi-app.py`: main file with app layout and callbacks
* `figures.py`: figure specifications
* `config.py`: text for the app, plus a dictionary specifying what goes into each tab and which data should be used to make the relevant graph.
* `app_data.h5`: the data underlying the app
* `assets`: css galore


## Installing conda and creating environments

In order to use conda environments, install [Miniconda](https://conda.io/miniconda.html) or Anaconda if you don't have it yet.

There are two environments: `odi` and `odi-app`, the details of which are in yaml files (`environment_simulation.yaml` and `environment_app.py`). To install, use `conda env create -f /path/to/environment_xxx.yaml` with the correct path and filename.
