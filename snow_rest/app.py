from flask import Flask, make_response, jsonify, request, abort

import snow_session
import snow_procs

# Snowflake Session
session = snow_session.get_db_client()

# Set up REST API
app = Flask(__name__)

def error_response(e):
    resp = make_response(jsonify({'message': str(e)}))
    resp.status_code = 400
    resp.status = 'error.Bad Request'
    return resp

@app.route("/busy_airports", methods=["GET"])
def busy_airports():
    begin = request.args.get('begin') or None
    end = request.args.get('end') or None
    deparr = request.args.get('deparr') or None
    nrows = request.args.get('nrows') or None
    try:
        return make_response(jsonify(snow_procs.busy_airports(session, begin, end, deparr, nrows)))
    except Exception as e:
        return error_response(e)


@app.route("/airport_daily/<airport>", methods=["GET"])
def airport_daily(airport):
    begin = request.args.get('begin') or None
    end = request.args.get('end') or None
    try:
        return make_response(jsonify(snow_procs.airport_daily(session, airport, begin, end)))
    except Exception as e:
        return error_response(e)

@app.route("/airport_daily_carriers/<airport>", methods=["POST"])
def airport_daily_carriers(airport):
    begin = request.args.get('begin') or None
    end = request.args.get('end') or None
    deparr = request.args.get('deparr') or None
    try:
        return make_response(jsonify(snow_procs.airport_daily_carriers(session, airport, begin, end, deparr)))
    except Exception as e:
        return error_response(e)

if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
