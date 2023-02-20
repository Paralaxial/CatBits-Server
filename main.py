from scratcha import start
#from truncate import start
from flask import Flask, jsonify
from threading import Thread

app = Flask('')

import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
t = Thread(target=start)
t.start()


@app.route('/', methods=["GET"])
def home():
  respond = {"status": "Online"}
  resp = jsonify(respond)
  resp.headers['Content-Type'] = "text/plain"
  return resp


app.run(host='0.0.0.0', port=8080)
