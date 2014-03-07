# add a new facility type to the points
## facilities of a same type are given as a csv file of three columns: name, x, y
## for each point
##   calculate distance between each point and all facilities
##   assign the smallest distance facility name and distance to the point
from pymongo import MongoClient
from bson.objectid import ObjectId
import math
from config import MONGODB_HOST, MONGODB_PORT, MONGODB_DB, MONGODB_USER, MONGODB_PW, MONGODB_LOC_COLL,\
    MONGODB_MIN_DISTANCE_FIELD_NAME, MONGODB_MIN_DISTANCE_FACILITY_FIELD_NAME, NUM_POINTS_TO_PRINT,\
    EARTH_RADIUS, KM_MILE_FACTOR, FACILITY_FILE_DELIM, LOC_BATCH_SIZE
from datetime import datetime


def _get_current_time_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


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
    print '%s: starting add facility type %s to all points in MongoDB' % \
          (_get_current_time_str(), type_name)

    # connect to MongoDB
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    db = client[MONGODB_DB]
    db.authenticate(MONGODB_USER, MONGODB_PW)

    # parse csv to list of dicts
    facilities = list()
    for line in open(csv_path, 'r').readlines()[1:]:
        line_split = line.split(FACILITY_FILE_DELIM)
        name = line_split[0]
        x = float(line_split[1])
        y = float(line_split[2].split('\r\n')[0])
        facilities.append({'name': name, 'x': x, 'y': y})

    # insert facilities to MongoDB
    fac_coll = db[type_name]
    fac_coll.insert(facilities)

    # update location to contain min distance information
    loc_coll = db[MONGODB_LOC_COLL]
    print '%s: Connected to DB (Host: %s, Port: %d, DB: %s)' % (_get_current_time_str(), MONGODB_HOST, MONGODB_PORT, MONGODB_DB)

    index = 1
    for loc in loc_coll.find().batch_size(LOC_BATCH_SIZE):
        min_distance, min_distance_facility_name = _find_min_distance_facility_from_loc(loc, facilities)
        loc_coll.update({'_id': ObjectId(loc['_id'])},
                        {'$set': {type_name:
                                  {MONGODB_MIN_DISTANCE_FACILITY_FIELD_NAME: min_distance_facility_name,
                                   MONGODB_MIN_DISTANCE_FIELD_NAME: min_distance}}
                        })
        if index % NUM_POINTS_TO_PRINT == 0:
            print '%s: %d locations are processed' % (_get_current_time_str(), index)
        index += 1

    print '%s: total %d locations now started having type %s' % (_get_current_time_str(), index - 1, type_name)

    # disconnect from MongoDB
    print '%s: disconnecting from MongoDB and exiting' % _get_current_time_str()
    client.disconnect()


if __name__ == '__main__':
    # transportation
    #add_facility_type('./facilities/el_stops/yellow_el_stop.csv', 'yellow_el')
    #add_facility_type('./facilities/el_stops/purple_el_stop.csv', 'purple_el')
    #add_facility_type('./facilities/el_stops/red_el_stop.csv', 'red_el')
    #add_facility_type('./facilities/transportation/blue_el_stop.csv', 'blue_el')
    #add_facility_type('./facilities/transportation/any_el_stop.csv', 'any_el')
    #add_facility_type('./facilities/transportation/brown_el_stop.csv', 'brown_el')
    #add_facility_type('./facilities/transportation/green_el_stop.csv', 'green_el')
    #add_facility_type('./facilities/transportation/orange_el_stop.csv', 'orange_el')
    #add_facility_type('./facilities/transportation/pink_el_stop.csv', 'pink_el')
    #add_facility_type('./facilities/transportation/divvy_stations.csv', 'divvy')
    add_facility_type('./facilities/transportation/metra_stations.csv', 'metra')

    # government
    #add_facility_type('./facilities/government/fire_stations.csv', 'fire_stations')
    #add_facility_type('./facilities/government/police_stations.csv', 'police_stations')

    # business
    #add_facility_type('./facilities/business/animal_care.csv', 'animal_care')
    #add_facility_type('./facilities/business/children_services.csv', 'children_services')
    #add_facility_type('./facilities/business/late_hour_liquor.csv', 'late_hour_liquor')
    #add_facility_type('./facilities/business/liquor_stores.csv', 'liquor_stores')
    #add_facility_type('./facilities/business/spas.csv', 'spas')
    #add_facility_type('./facilities/business/taverns.csv', 'taverns')
    #add_facility_type('./facilities/business/tobacco.csv', 'tobacco')

    #add_facility_type('./facilities/business/tobacco.csv', 'cvs')
    #add_facility_type('./facilities/business/tobacco.csv', 'enterprise')
    #add_facility_type('./facilities/business/tobacco.csv', 'ffc')
    #add_facility_type('./facilities/business/tobacco.csv', 'hertz')
    #add_facility_type('./facilities/business/tobacco.csv', 'starbucks')
    #add_facility_type('./facilities/business/tobacco.csv', 'target')
    #add_facility_type('./facilities/business/tobacco.csv', 'walgreens')