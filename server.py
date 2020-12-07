from flask import Flask, request
import json
import uuid
from util import Address

app = Flask(__name__)

addresses = set()


@app.route("/allocate", methods=["POST"])
def allocate():
    ip = request.remote_addr
    port = request.form.get("port")

    addresses.add((ip, port))

    return json.dumps({
        "addresses": list(addresses)
    })


@app.route("/deallocate", methods=["POST"])
def deallocate():
    ip = request.remote_addr
    port = request.form.get("port")
    addresses.remove((ip, port))
    return "ok"


@app.route("/keep_alive", methods=["GET"])
def keep_alive():
    return json.dumps({
        "addresses": list(addresses)
    })


if __name__ == '__main__':
    app.run("0.0.0.0", port=1140)
