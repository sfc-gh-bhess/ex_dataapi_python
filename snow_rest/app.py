import logging
import sys
from flask import Flask, make_response, jsonify, request, abort

import snow_session
import snow_procs

# Set Logging Level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Snowflake Session
session = snow_session.get_db_client()

# Set up REST API
app = Flask(__name__)

@app.route("/busy_airports", methods=["GET"])
def busy_airports():
    begin = request.args.get('begin') or None
    end = request.args.get('end') or None
    deparr = request.args.get('deparr') or None
    nrows = request.args.get('nrows') or None
    return make_response(jsonify(snow_procs.busy_airports(session, begin, end, deparr, nrows)))

@app.route("/airport_daily/<airport>", methods=["GET"])
def airport_daily(airport):
    begin = request.args.get('begin') or None
    end = request.args.get('end') or None
    return make_response(jsonify(snow_procs.airport_daily(session, airport, begin, end)))

@app.route("/airport_daily_carriers/<airport>", methods=["POST"])
def airport_daily_carriers(airport):
    begin = request.args.get('begin') or None
    end = request.args.get('end') or None
    deparr = request.args.get('deparr') or None
    return make_response(jsonify(snow_procs.airport_daily_carriers(session, airport, begin, end, deparr)))

if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
