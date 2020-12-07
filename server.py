from flask import Flask, request
import json
import uuid

app = Flask(__name__)

addresses = {}  # id : address


@app.route("/allocate", methods=["POST"])
def allocate():
    ip = request.remote_addr
    port = request.form.get("port")

    id_ = str(uuid.uuid4())
    addresses[id_] = (ip, port)

    return json.dumps({
        "id": id_,
        "addresses": addresses.values()
    })


@app.route("/deallocate", methods=["POST"])
def deallocate():
    id_ = request.form.get("id")
    addresses.pop(id_)
    return "ok"


@app.route("/keep_alive", methods=["GET"])
def keep_alive():
    return json.dumps({
        "addresses": addresses.values()
    })

