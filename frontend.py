from backend import get_locs, get_facility_types
from config import NUM_CRITERIA, POSSIBLE_DISTANCE_OPTIONS, NULL_STRING, NO_RESULT_FOUND_MSG, NON_FACILITY_KEYS, \
    MORE_THAN_LIMIT_FOUND_MSG, APP_SECRET_KEY
from flask import Flask, render_template, request, flash
app = Flask(__name__)
app.secret_key = APP_SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def main():
    facility_types = get_facility_types()
    if request.method == 'GET':
        return render_template('main.html', facility_types=facility_types, num_criteria=NUM_CRITERIA,
                               possible_distance_options=POSSIBLE_DISTANCE_OPTIONS, null_string=NULL_STRING)
    else:
        criteria = dict()
        projections = dict()

        for non_facility_id in NON_FACILITY_KEYS:
            projections[non_facility_id] = 1

        # create criteria and projections dicts
        for i in range(0, NUM_CRITERIA):
            ftype = request.form['type_%d' % i]
            distance = request.form['distance_%d' % i]

            if ftype != NULL_STRING and distance != NULL_STRING and ftype and distance:
                criteria['%s.md' % ftype] = dict()
                criteria['%s.md' % ftype]['$lt'] = float(distance)
                projections[ftype] = 1

        # search for locations based on criteria
        results, more_than_limit_flg, no_result_flg = get_locs(criteria, projections)
        if more_than_limit_flg:
            flash(MORE_THAN_LIMIT_FOUND_MSG, 'info')
        if no_result_flg:
            flash(NO_RESULT_FOUND_MSG, 'info')

        return render_template('main.html', facility_types=facility_types, num_criteria=NUM_CRITERIA,
                               possible_distance_options=POSSIBLE_DISTANCE_OPTIONS, null_string=NULL_STRING,
                               results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
