# fastapi-flask-benchmark
A simple benchmark for [Fast API](https://fastapi.tiangolo.com/) vs. [flask](https://flask.palletsprojects.com/en/1.1.x/).

## Setup
This uses `poetry` to manage dependencies, so you should just need to [install poetry](https://python-poetry.org/docs/#installation), and then run `poetry install` to start.

## Benchmarking

First, you need to start the webserver you want to benchmark. Then, you want to choose a benchmark to run.

### Start webservers
This will run the webserver on `127.0.0.1:5000` with 4 [uvicorn](https://github.com/encode/uvicorn) workers, using [gunicorn](https://gunicorn.org/) as the webserver.

- `start_fastapi.sh`: starts FastAPI webserver. Supports async and sync methods.
- `start_flask.sh`: starts Flask webserver. Only supports sync methods.


