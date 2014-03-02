# add a new facility type to the points
## facilities of a same type are given as a csv file of three columns: name, x, y
## for each point
##   calculate distance between each point and all facilities
##   assign the smallest distance facility name and distance to the point
from pymongo import MongoClient
from bson.objectid import ObjectId
import math
from config import MONGODB_HOST, MONGODB_PORT, MONGODB_DB, MONGODB_COLL,\
    MONGODB_MIN_DISTANCE_FIELD_NAME, MONGODB_MIN_DISTANCE_FACILITY_FIELD_NAME, NUM_POINTS_TO_PRINT,\
    EARTH_RADIUS, KM_MILE_FACTOR, FACILITY_FILE_DELIM

def _calculate_distance_between_two_points(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = EARTH_RADIUS

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d


def _find_min_distance_facility_from_loc(loc, facilities):
    for i in range(0, len(facilities)):
        facilities[i]['distance'] = _calculate_distance_between_two_points((loc['x'], loc['y']),
                                                                           (facilities[i]['x'], facilities[i]['y']))
    min_distance_facility = sorted(facilities, key=lambda facility: facility['distance'], reverse=False)[0]
    return min_distance_facility['distance'] * KM_MILE_FACTOR, min_distance_facility['name']


def add_facility_type(csv_path, type_name):
    print 'Starting add facility type %s to all points in MongoDB' % type_name

    # connect to MongoDB
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    db = client[MONGODB_DB]
    db.authenticate(MONGODB_USER, MONGODB_PW)
    coll = db[MONGODB_COLL]
    print 'Connected to DB (Host: %s, Port: %d, DB: %s)' % (MONGODB_HOST, MONGODB_PORT, MONGODB_DB)

    facilities = list()
    for line in open(csv_path, 'r').readlines()[1:]:
        line_split = line.split(FACILITY_FILE_DELIM)
        name = line_split[0]
        x = float(line_split[1])
        y = float(line_split[2].split('\r\n')[0])
        facilities.append({'name': name, 'x': x, 'y': y})

    index = 1
    for loc in coll.find():
        min_distance, min_distance_facility_name = _find_min_distance_facility_from_loc(loc, facilities)
        coll.update({'_id': ObjectId(loc['_id'])}, {'$set': {type_name: {MONGODB_MIN_DISTANCE_FACILITY_FIELD_NAME: min_distance_facility_name, MONGODB_MIN_DISTANCE_FIELD_NAME: min_distance}}})
        if index % NUM_POINTS_TO_PRINT == 0:
            print '%d locations are processed' % (index)
        index += 1

    print 'Total %d locations now started having type %s' % (index - 1, type_name)

    # disconnect from MongoDB
    print 'Disconnecting from MongoDB and exiting'
    client.disconnect()


if __name__ == '__main__':
    #add_facility_type('./facilities/el_stops/yellow_el_stop.csv', 'yellow_el')
    #add_facility_type('./facilities/el_stops/purple_el_stop.csv', 'purple_el')
    #add_facility_type('./facilities/el_stops/red_el_stop.csv', 'red_el')
    #add_facility_type('./facilities/el_stops/blue_el_stop.csv', 'blue_el')
    add_facility_type('./facilities/el_stops/any_el_stop.csv', 'any_el')
    add_facility_type('./facilities/el_stops/brown_el_stop.csv', 'brown_el')
    add_facility_type('./facilities/el_stops/green_el_stop.csv', 'green_el')
    add_facility_type('./facilities/el_stops/orange_el_stop.csv', 'orange_el')
    add_facility_type('./facilities/el_stops/pink_el_stop.csv', 'pink_el')