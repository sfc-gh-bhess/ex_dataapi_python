# ex_dataapi_python
Blog Example for Snowflake Data API in Python and Docker

This repository is an example of building a data API on data hosted
in Snowflake. It accompanies this Medium post describing how to build
APIs using Python and Docker for Snowflake.

## REST API for OAG Flight Schedule data
This example puts a simple data API to answer some basic questions of
the OAG Flight Schedule data in the Snowflake Marketplace.

The data is available in the Snowflake Marketplace [here](https://app.snowflake.com/marketplace/listing/GZ1M7Z2MQ39).

There are 3 API endpoints for this data:
* `busy_airports` - this will list the top airpots in terms of flight departures (or arrivals). It can be
  customized with the following optional parameters:
  * `deparr` - whether to consider departures (`DEPAPT`) or arrivals (`ARRAPT`). Default is `DEPAPT`.
  * `nrows` - how many airports to show. Default is `20`.
  * `begin` - start date to include. Default is all the data.
  * `end` - end date to include. Default is all the data.
* `airport_daily` - this will show the daily departures and arrivals for the specified airport. 
  The airport code is included as a path variable (i.e., `/airport_daily/{airport_code}`).
  * `airport_code` - the 3-letter airport code to consider. Required.
  * `begin` - start date to include. Default is all the data.
  * `end` - end date to include. Default is all the data.
* `airport_daily_carriers` - this will show the daily departures (or arrivals) for various 
  airline carriers for the specified airport. The airport code is included as a path variable
  (i.e., `/airport_daily_carriers/{airport_code})
  * `airport_code` - the 3-letter airport code to consider. Required.
  * `deparr` - whether to consider departures (`DEPAPT`) or arrivals (`ARRAPT`). Default is `DEPAPT`.
  * `begin` - start date to include. Default is all the data.
  * `end` - end date to include. Default is all the data.

The `busy_airports` and `airport_daily` endpoints are accessed via the `GET` verb. 
The `airport_daily_carriers` endpiont is accessed via the `POST` verb.
All parameters (other than the `airport_code`, which is supplied as a path variable) are 
supplied as query parameters.

## Snowflake Setup for Example
To deploy this example you will need to get the OAG Flight Schedule data imported into your
Snowflake account. It is advised to create a role to access this data, and create a user (and password)
that the example will use to access this data, and grant that user the role. This user/password
will be used by the Python functions to access Snowflake.

To configure the API you will need to provide the following information about 
your Snowflake setup:
* Snowflake account identifier
* Snowflake username - who has access to the OAG data share in your account
* Snowflake password
* Snowflake warehouse to use
* Name of the database in your Snowflake account that houses the imported OAG data share.

This information should be placed in the `snow_rest/config.json` file. That
file is not included, but the file `snow_rest/config.json.example` is a template
to follow to create that file.

## Python Application and Dockerfile
This repo provides a Python implementation of the REST API using
the Flask Python package. The repo consists of 3 main Python files
in the `snow_rest` directory:
* `app.py` - the main Flask application, responsible for gathering
    arguments and calling the functions in `snow_procs.py`
* `snow_procs.py` - calls Snowflake to get the necessary data
* `snow_session.py` - responsible for making the connection to Snowflake

You can run this application locally (after installing the Python packages
in `requirements.txt`) by running:
```
make run_local
```

or
```
cd snow_rest
python app.py
```

The Python application will listen to all network interfaces and binds to
the port `8080`. If you would like to modify this, edit the `app.run` 
call at the end of the `app.py` file. If you do change the port, you will
need to update the Dockerfile (see next section) and the Makefile

### Building the Docker container
This repo also includes a Dockerfile to create a Docker image. To simplify
things, the Docker command is included in the Makefile, allowing you to
build the Docker container via the following command:
```
make docker
```

The name of the image is configurable. You can edit the Makefile to 
change the value of `DOCKERIMAGENAME`. 

## Testing the API

### Start Docker image locally
To start the Docker image locally, you can run:
```
make run
```
The API will be available at `http://localhost:8080` (unless you changed
the port number above).

### Example Queries
In the following examples, `APIROOT` is the output from the stack, `WEBUSER` is the
username to protect the API, and `WEBPASSWORD` is the password to protect the API.

1. Show the 20 busiest airports based on departures using the full data set:
```
curl http://localhost:8080/busy_airports
```

2. Show the 10 busiest airports based on arrivals in the date range of July 1-5, 2022:
```
curl http://localhost:8080/busy_airports?deparr=ARRAPT&nrows=10&begin=2022-07-01&end=2022-07-05
```

3. Show the daily departures and arrivals for `BOS` in the date range of July 1-5, 2022:
```
curl http://localhost:8080/airport_daily/BOS?begin=2022-07-01&end=2022-07-05
```

4. Show the daily arrivals for select carriers for `BOS` in the date range of July 1-5, 2022:
```
curl -X POST http://localhost:8080/airport_daily_carriers/BOS?begin=2022-07-01&end=2022-07-05&deparr=ARRAPT
```

## Considerations
One major thing missing from this example is authentication to protect
the API from misuse. This is achievable via Flask or other Python packages.
It was omitted so we could focus on the API itself and how to communicate
with Snowflake. However, it is never advisable to go into production with 
an API without authentication.
