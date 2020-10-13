import csv
import multiprocessing
import pathlib
import time
from typing import Callable, List

import benchmark
import start_webserver
from helpers import constants

OUTPUT_DIR = "./output"
RESULT_PREFIX = "results_"

WEBSERVERS = [
    ("Flask", start_webserver.start_flask),
    ("FastAPI_sync", start_webserver.start_fast),
    ("FastAPI_async", start_webserver.start_fast_async)
]


def start_webserver_background(start_fn: Callable, kwargs=None, initialization_time=5) -> multiprocessing.Process:
    p = multiprocessing.Process(target=start_fn, kwargs=kwargs if kwargs else {})
    p.start()
    time.sleep(initialization_time)
    return p


def start_wait_server() -> multiprocessing.Process:
    return start_webserver_background(start_webserver.start_fast_async, kwargs={"port": constants.WAIT_PORT})


def run_benchmark(benchmark_instance: benchmark.Benchmark) -> List[List[str]]:
    results: List[List[str]] = []

    for name, start_fn in WEBSERVERS:
        def setup():
            start_wait_server()
            start_webserver_background(start_fn)

        def teardown():
            start_webserver.kill_webservers()

        result = benchmark.run_benchmark(benchmark_instance, setup, teardown)
        results.append([name] + result)

    return results


if __name__ == "__main__":
    for benchmark_instance in benchmark.BENCHMARKS:
        print("Running benchmarks for", benchmark_instance.name())
        results = run_benchmark(benchmark_instance)
        file_path = pathlib.Path(OUTPUT_DIR) / "".join((benchmark_instance.name(), ".csv"))
        with open(file_path, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["name"] + benchmark.HEADERS)
            for result in results:
                writer.writerow(result)
