from os import environ
MONGODB_HOST = 'sunghopark.info'
MONGODB_PORT = 27017
MONGODB_DB = 'chicago_dev'
MONGODB_COLL = 'locs'
MONGODB_USER = environ['MONGODB_USER']
MONGODB_PW = environ['MONGODB_PW']
MAX_NUM_SEARCH_RESULTS = 25
MONGODB_MIN_DISTANCE_FIELD_NAME = 'md'
MONGODB_MIN_DISTANCE_FACILITY_FIELD_NAME = 'mdfn'

APP_SECRET_KEY = environ['CHICAGO_APP_SECRET_KEY']

_ID_KEY = '_id'
X_KEY = 'x'
Y_KEY = 'y'
NON_FACILITY_KEYS = [_ID_KEY, X_KEY, Y_KEY]

NUM_CRITERIA = 5
POSSIBLE_DISTANCE_OPTIONS = [0.1, 0.2, 0.5, 1.0]  # unit: miles
NULL_STRING = 'null'
MORE_THAN_LIMIT_FOUND_MSG = 'Too many results were found! I am only showing %s results.' % MAX_NUM_SEARCH_RESULTS
NO_RESULT_FOUND_MSG = 'Sorry - I could not find any location that meets your criteria. Try again with more general criteria.'