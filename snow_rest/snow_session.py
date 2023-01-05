import logging
import json
from snowflake.snowpark import Session

# Set Logging Level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Load configuration
creds = json.load(open('config.json', 'r'))

## SNOWFLAKE CONNECTION
session = None
def get_db_client():
    global session
    if session is None:
        try:
            session = Session.builder.configs(creds).create()
            print("Connection established")
        except Exception as ex:
            logger.error('Failed to connect: ' + str(ex))
            raise
    return session