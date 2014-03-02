# config file for ETL
from os import environ
from decimal import Decimal, getcontext
MONGODB_HOST = 'sunghopark.info'
MONGODB_PORT = 27017
MONGODB_DB = 'chicago_dev'
MONGODB_USER = environ['MONGODB_USER']
MONGODB_PW = environ['MONGODB_PW']
MONGODB_COLL = 'locs'
MONGODB_MIN_DISTANCE_FIELD_NAME = 'md'
MONGODB_MIN_DISTANCE_FACILITY_FIELD_NAME = 'mdfn'

getcontext().prec = 8
_NUM_POINTS_ALONG_X = 10
_NUM_POINTS_ALONG_Y = 20

X_MIN = Decimal(41.647166)
X_MAX = Decimal(42.016700)
X_INTERVAL = (X_MAX - X_MIN) / _NUM_POINTS_ALONG_X

Y_MIN = Decimal(-87.945152)
Y_MAX = Decimal(-87.528641)
Y_INTERVAL = (Y_MAX - Y_MIN) / _NUM_POINTS_ALONG_Y

NUM_POINTS_TO_PRINT = 50

EARTH_RADIUS = 6371  # km
KM_MILE_FACTOR = 0.621

FACILITY_FILE_DELIM = '|'