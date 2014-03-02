# initialize MongoDB
## drop collection if exists
## create a collection
## add points based on x_min, x_max, y_min, y_max, x_interval, y_interval to the collection
from config import MONGODB_HOST, MONGODB_PORT, MONGODB_DB, MONGODB_COLL, X_MIN, X_MAX, X_INTERVAL, \
    Y_MIN, Y_MAX, Y_INTERVAL, NUM_POINTS_TO_PRINT
from pymongo import MongoClient
from numpy import arange


if __name__ == '__main__':
    # connect to MongoDB
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    db = client[MONGODB_DB]
    print "Connected to DB (Host: %s, Port: %d, DB: %s)" % (MONGODB_HOST, MONGODB_PORT, MONGODB_DB)

    # check collection already exists and if so, drop it
    if MONGODB_COLL in db.collection_names(False):
        print "Collection %s already exists" % MONGODB_COLL
        db.drop_collection(MONGODB_COLL)
        print "Collection %s is dropped" % MONGODB_COLL

    # create a new collection
    db.create_collection(MONGODB_COLL)
    print "Collection %s is created" % MONGODB_COLL

    # insert points based on configuration
    coll = db[MONGODB_COLL]
    index = 1
    for x in arange(X_MIN, X_MAX, X_INTERVAL):
        for y in arange(Y_MIN, Y_MAX, Y_INTERVAL):
            coll.insert({'x': float(x), 'y': float(y)})
            if index % NUM_POINTS_TO_PRINT == 0:
                print '%d points are added to MongoDB' % index
            index += 1

    print 'Total %d points are added to MongoDB' % (index - 1)

    print 'Disconnecting from MongoDB and exiting'
    client.disconnect()