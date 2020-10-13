from time import sleep

from flask import Flask, request, jsonify

from helpers import request_helpers, work_helper, database_helper_sync

app = Flask(__name__)


@app.route("/wait")
def wait():
    sleep(1)
    return {"wait": "finished"}


@app.route("/parse", methods=["POST"])
def parse():
    return jsonify(request.json)


@app.route("/fetch")
def fetch():
    request_helpers.make_sync_wait_request()
    return {"status": "done"}


@app.route("/work")
def work():
    work_helper.run_model()
    return {"status": "done"}


@app.route("/db")
def database():
    database_helper_sync.make_fetch_then_delete_objects()
    return {"status": "done"}
