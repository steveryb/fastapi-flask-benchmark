import argparse
import subprocess
from typing import List, Callable

from helpers import constants


class Benchmark(object):
    def run(self) -> List[str]:
        raise NotImplementedError("Did not implement the run for benchmark")

    def name(self) -> str:
        return type(self).__name__

    def wrk(self, route, threads=12, connections=200, duration=60, timeout=100,
            script="wrk_scripts/print_to_csv.lua", ) -> List[str]:
        """
        Run the wrk command against the given route. Assumes host is 127.0.0.1:5000.

        :param route:
        :return: results from that benchmark according to the print_to_csv.lua spec
        """
        print("Benchmark starting:", self.name())
        run_output = subprocess.run(
            [constants.WRK_PATH, f"{constants.WEB_SERVER_HOST_WITH_PORT}{route}", "-s", script, f"-t{threads}",
             f"-c{connections}",
             f"-d{duration}s", "--timeout", f"{timeout}s", ], capture_output=True, text=True)
        print("Benchmark ending:", self.name())
        print("Benchmark output")
        print("stdout:", run_output.stdout)
        print("sterr:", run_output.stderr)
        # only care about the last line, as that has the csv output
        last_line = run_output.stdout.strip().split("\n")[-1]
        return last_line.split(",")  # split that csv output


class WaitBenchmark(Benchmark):
    def run(self) -> List[str]:
        return self.wrk("/wait")


class ParseBenchmark(Benchmark):
    def run(self) -> List[str]:
        return self.wrk("/parse", script="wrk_scripts/json_with_print_to_csv.lua")


class FetchBenchmark(Benchmark):
    def run(self) -> List[str]:
        return self.wrk("/fetch")


class WorkBenchmark(Benchmark):
    def run(self) -> List[str]:
        return self.wrk("/work")


class DatabaseBenchmark(Benchmark):
    def run(self) -> List[str]:
        return self.wrk("/db")


BENCHMARKS = [
    WaitBenchmark(),
    ParseBenchmark(),
    FetchBenchmark(),
    WorkBenchmark(),
    DatabaseBenchmark()
]

HEADERS = [
    "latency min",
    "latency p50",
    "latency p75",
    "latency p90",
    "latency p99",
    "latency p99.9",
    "latency max",
    "latency mean",
    "duration",
    "# requests",
    "# error status",
    "# error read",
    "# error timeout"
]


def format_benchmark(results: List[List[str]]) -> str:
    return "\n".join(",".join(row) for row in [HEADERS] + results)


def empty_function():
    pass


def run_benchmark(benchmark: Benchmark, setup: Callable, teardown: Callable) -> List[str]:
    setup()
    results = benchmark.run()
    teardown()
    return results


def run_benchmarks(setup=empty_function, teardown=empty_function) -> List[List[str]]:
    results: List[List[str]] = []
    for benchmark in BENCHMARKS:
        results.append([benchmark.name()] + run_benchmark(benchmark, setup, teardown))
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wrapper around wrk to facilitate benchmarking")
    args = parser.parse_args()

    print(format_benchmark(run_benchmarks(empty_function, empty_function)))
