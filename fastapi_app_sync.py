import time

from fastapi import FastAPI

app = FastAPI()
from helpers import database_helper_sync, request_helpers, work_helper
from fastapi_models import *

database_helper_sync.create_all_models()


@app.get("/wait")
def wait():
    time.sleep(1)
    return {"wait": "finished"}


@app.post("/parse")
def parse(people: People):
    return people


@app.get("/fetch")
def fetch():
    request_helpers.make_sync_wait_request()
    return {"status": "done"}


@app.get("/work")
def work():
    work_helper.run_model()
    return {"status": "done"}


@app.get("/db")
def database():
    database_helper_sync.make_fetch_then_delete_objects()
    return {"status": "done"}
