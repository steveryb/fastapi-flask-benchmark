import asyncio

from fastapi import FastAPI

app = FastAPI()
from fastapi_models import *
from helpers import database_helper_async, request_helpers, work_helper


@app.get("/wait")
async def async_wait():
    await asyncio.sleep(1)
    return {"wait": "finished"}


@app.post("/parse")
async def async_parse(people: People):
    return people


@app.get("/fetch")
async def async_fetch():
    await request_helpers.make_async_wait_request()
    return {"status": "done"}


@app.get("/work")
async def async_fetch():
    work_helper.run_model()
    return {"status": "done"}


@app.on_event("startup")
async def startup():
    await database_helper_async.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database_helper_async.database.disconnect()


@app.get("/db")
async def async_db():
    await database_helper_async.make_fetch_then_delete_objects()
    return {"status": "done"}
