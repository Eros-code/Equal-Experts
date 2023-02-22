import pandas as pd
from assets.sql_wrapper import SQLConnection
import numpy as np

import os
import dotenv

dotenv.load_dotenv(override=True)

username = os.environ['SQL_USERNAME']
host = os.environ['SQL_HOST']
password = os.environ['SQL_PASSWORD']
db = os.environ['DBNAME']
port = os.environ['port']

def db_connect():
    sql = SQLConnection(db, username, password) ## allows us to perform sql queries on the database
    return sql

