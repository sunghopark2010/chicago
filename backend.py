from pymongo import MongoClient
from config import MONGODB_HOST, MONGODB_PORT, MONGODB_DB, MONGODB_COLL, MAX_NUM_SEARCH_RESULTS, NON_FACILITY_KEYS, \
    X_KEY, Y_KEY, MONGODB_MIN_DISTANCE_FIELD_NAME, MONGODB_MIN_DISTANCE_FACILITY_FIELD_NAME, NO_RESULT_FOUND_MSG


def _make_proper(raw_key):
    return ' '.join([word.capitalize() for word in raw_key.split('_')])


def get_facility_types():
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    db = client[MONGODB_DB]
    coll = db[MONGODB_COLL]
    a_loc = coll.find_one()
    query_keys = sorted(filter(lambda key: key not in NON_FACILITY_KEYS, a_loc.keys()))
    display_keys = map(lambda raw_key: _make_proper(raw_key), query_keys)
    client.disconnect()
    return zip(query_keys, display_keys)


def get_locs(criteria, projections):
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    db = client[MONGODB_DB]
    coll = db[MONGODB_COLL]
    locs = coll.find(criteria, projections).limit(MAX_NUM_SEARCH_RESULTS)
    results = list()
    for loc in locs:
        mdf = list()
        for projection_key in projections.keys():
            if projection_key not in NON_FACILITY_KEYS:
                mdf.append({'field_name': _make_proper(projection_key), 'md': loc[projection_key]['md'],
                            'mdfn': loc[projection_key]['mdfn']})

        results.append({X_KEY: loc[X_KEY], Y_KEY: loc[Y_KEY], 'mdf': mdf})
    client.disconnect()
    return results


def _get_keys_from_locs(locs):
    keys = [X_KEY, Y_KEY]
    return keys + map(lambda raw_key: _make_proper(raw_key),
                      filter(lambda key: key not in NON_FACILITY_KEYS, locs[0].keys()))


def _convert_locs_dict_to_list(locs, keys):
    values = list()
    for loc in locs:
        value = list()
        for key in keys:
            if key in [X_KEY, Y_KEY]:
                value.append(loc[key])
            else:
                pair = list()
                pair.append(loc[key][MONGODB_MIN_DISTANCE_FIELD_NAME])
                pair.append(loc[key][MONGODB_MIN_DISTANCE_FACILITY_FIELD_NAME])
                value.append(pair)
        values.append(value)
    return values