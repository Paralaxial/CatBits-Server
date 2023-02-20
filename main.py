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


@app.route('/')
def home():
  respond = {"status": "Online"}
  return jsonify(respond)


app.run(host='0.0.0.0', port=8080)
