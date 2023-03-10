from snowflake.snowpark.functions import col
import snowflake.snowpark.functions as f
import json
import sys
import datetime

# Load configuration
creds = json.load(open('config.json', 'r'))
table = f"{creds['database']}.PUBLIC.OAG_SCHEDULE"

def busy_airports(session, begin, end, deparr, nrows):
    df = session.table(table)
    if begin and end:
        try:
            d_begin = datetime.date.fromisoformat(begin)
            d_end = datetime.date.fromisoformat(end)
            df = df.filter((col('FLIGHT_DATE') >= d_begin) & (col('FLIGHT_DATE') <= d_end))
        except ValueError as ex:
            print('Bad dates provided: ' + str(ex), file=sys.stderr)
            raise ValueError("Error: Bad dates provided")
    deparr = deparr if deparr == 'ARRAPT' else 'DEPAPT'
    try:
        nrows = int(nrows or 20)
    except ValueError as ex:
        print('nrows must be an integer', file=sys.stderr)
        raise ValueError('Error: nrows must be an integer')
    df = df.group_by(col(deparr)) \
                    .agg(f.count(deparr).alias('ct')) \
                    .sort(col('ct').desc()) \
                    .limit(nrows) 
    try:
        retval = [x.as_dict() for x in df.to_local_iterator()]
    except Exception as ex:
        print('Failed to retrieve data frame: ' + str(ex), file=sys.stderr)
        raise Exception("Error reading from Snowflake. Check the logs for details.")
    return retval

def airport_daily(session, apt, begin, end):
    df = session.table(table)
    if begin and end:
        try:
            d_begin = datetime.date.fromisoformat(begin)
            d_end = datetime.date.fromisoformat(end)
            df = df.filter((col('FLIGHT_DATE') >= d_begin) & (col('FLIGHT_DATE') <= d_end))
        except ValueError as ex:
            print('Bad dates provided: ' + str(ex), file=sys.stderr)
            raise ValueError("Error: Bad dates provided")
    df = df.group_by(col('FLIGHT_DATE')) \
        .agg([ \
                f.sum(f.when(col('DEPAPT') == apt, f.lit(1)).otherwise(f.lit(0))).alias('depct'), \
                f.sum(f.when(col('ARRAPT') == apt, f.lit(1)).otherwise(f.lit(0))).alias('arrct') \
            ]) \
        .sort(col('FLIGHT_DATE').asc())
    try:
        retval = [x.as_dict() for x in df.to_local_iterator()]
    except Exception as ex:
        print('Failed to retrieve data frame: ' + str(ex), file=sys.stderr)
        raise Exception("Error reading from Snowflake. Check the logs for details.")
    return retval

airline_list = {
        'AA':'American', 
        'DL':'Delta', 
        'UA':'United', 
        'B6':'JetBlue', 
        'WN':'Southwest', 
        'AS':'Alaska'
    }
def airport_daily_carriers(session, apt, begin, end, deparr):
    df = session.table(table)
    if begin and end:
        try:
            d_begin = datetime.date.fromisoformat(begin)
            d_end = datetime.date.fromisoformat(end)
            df = df.filter((col('FLIGHT_DATE') >= d_begin) & (col('FLIGHT_DATE') <= d_end))
        except ValueError as ex:
            print('Bad dates provided: ' + str(ex), file=sys.stderr)
            raise ValueError("Error: Bad dates provided")
    deparr = deparr if deparr == 'ARRAPT' else 'DEPAPT'
    df = df.filter(col('CARRIER').isin(list(airline_list.keys()))) \
        .filter(col(deparr) == apt) \
        .group_by([col('FLIGHT_DATE'), col('CARRIER')]) \
        .agg(f.count('FLIGHT_DATE').alias('ct')) \
        .sort(col('FLIGHT_DATE').asc())
    try:
        retval = [x.as_dict() for x in df.to_local_iterator()]
    except Exception as ex:
        print('Failed to retrieve data frame: ' + str(ex), file=sys.stderr)
        raise Exception("Error reading from Snowflake. Check the logs for details.")
    return retval

