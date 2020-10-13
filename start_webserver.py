import argparse
import subprocess

from helpers import constants

FAST = "fastapi_app_sync:app"
FLASK = "flask_app:app"
FAST_ASYNC = "fastapi_app_async:app"


def start_fast(address=constants.WEBSERVER_ADDRESS, port=constants.DEFAULT_PORT, workers=constants.DEFAULT_WORKERS):
    start_webserver(FAST, address, port, workers, uvicorn=True)


def start_fast_async(address=constants.WEBSERVER_ADDRESS, port=constants.DEFAULT_PORT,
                     workers=constants.DEFAULT_WORKERS):
    start_webserver(FAST_ASYNC, address, port, workers, uvicorn=True)


def start_flask(address=constants.WEBSERVER_ADDRESS, port=constants.DEFAULT_PORT, workers=constants.DEFAULT_WORKERS):
    start_webserver(FLASK, address, port, workers, uvicorn=False)


def start_webserver(name, address=constants.WEBSERVER_ADDRESS, port=constants.DEFAULT_PORT,
                    workers=constants.DEFAULT_WORKERS, uvicorn=False):
    args = ["poetry", "run", "gunicorn", name, "-b", f"{address}:{port}", "-w", str(workers)]
    if uvicorn:
        args += ["-k", "uvicorn.workers.UvicornWorker"]
    subprocess.run(args)


def kill_webservers():
    subprocess.run(["pkill", "-f", "gunicorn"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Helper script to start webservers")

    # get the webserver to run
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--name', help="name of the app to run")
    group.add_argument('--fast', help="start fastAPI", action="store_true")
    group.add_argument('--flask', help="start flask", action="store_true")
    group.add_argument('--fast_async', help="start fastAPI with async methods", action="store_true")

    # optionally get the port
    parser.add_argument('--port', help="The port to run the webserver on", default=constants.DEFAULT_PORT)
    args = parser.parse_args()

    name = ""
    if args.name:
        name = args.name
    elif args.fast:
        start_fast(port=args.port)
    elif args.flask:
        start_flask(port=args.port)
    elif args.fast_async:
        start_fast_async(port=args.port)
    else:
        raise NotImplementedError("Did not pass a supported name")
    start_webserver(name, port=args.port)
