# fastapi-flask-benchmark
A simple benchmark for [Fast API](https://fastapi.tiangolo.com/) vs. [flask](https://flask.palletsprojects.com/en/1.1.x/).

## Setup
This uses `poetry` to manage dependencies, so you should just need to [install poetry](https://python-poetry.org/docs/#installation), and then run `poetry install` to start.

If you're running this yourself, you'll have to change a couple constants because I ~~was too lazy to fix them~~ scoped these out of the initial release. Search for `#CHANGEME` for a hopefully complete list. 

## Run benchmarks

Assuming all goes well, you should be able to run your own benchmarks using `poetry run python benchmark_runner.py`. If all goes well, this should populate `output` with some new CSVs (you can check by seeing if they change with `git status`). 

## View analysis

For those not willing to try get this working on their machine, I've included [some analysis](analysis/benchmark_analysis.ipynb) in iPython notebook form. The tl;dr: FastAPI outperforms Flask in cases where there is a lot of waiting for I/O, Flask massively outperforms FastAPI if there's a lot of JSON to parse, and is faster than FastAPI for CPU heavy workloads though that data might be too close to make definitive judgements on.
