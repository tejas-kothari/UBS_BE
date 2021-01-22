import time
import ast
from flask import Flask, request
from flask_cors import CORS
import pandas as pd
from parser import seriesToDict, dfToDict
from random import randrange

print("reading csv...")
startups = pd.read_csv("csv/hitech_startups.csv")
funding = pd.read_csv("csv/hitech_funding.csv")
funding['lead_investor_uuids'] = funding['lead_investor_uuids'].str.split(',')
investors = pd.read_csv("csv/hitech_investors.csv")
print("done reading csv")

app = Flask(__name__)
CORS(
    app,
    origins=[r'http://localhost:.*', r'^https:\/\/temg4952a-team1.*.web\.app'])


@app.route("/time")
def get_current_time():
    return {"time": time.time()}


@app.route("/get_startup")
def get_startup():
    uuid = request.args.get('uuid')
    startup_row = startups[startups["uuid"] == uuid].iloc[0]
    startup_info = seriesToDict(startup_row)
    return startup_info


@app.route("/get_startup_funding")
def get_startup_funding():
    uuid = request.args.get('uuid')
    funding_df = funding[funding["org_uuid"] == uuid]
    investors_uuids = funding_df['lead_investor_uuids']
    funding_df = funding_df.drop('lead_investor_uuids', axis=1)
    funding_info = dfToDict(funding_df)

    for index, investors_uuids_array in investors_uuids.iteritems():
        investor_info = {}
        if not isinstance(investors_uuids_array, float):
            for array_index, investors_uuid in enumerate(
                    investors_uuids_array):
                investor_info[array_index] = seriesToDict(
                    investors[investors['uuid'] == investors_uuid].iloc[0])

        funding_info[index]['investors'] = investor_info

    return funding_info


@app.route("/get_startup_list")
def get_startup_list():
    startup_list = {}
    for num in range(0, 50):
        index = randrange(0, len(startups))
        startup_row = startups.iloc[index][[
            'uuid', 'name', 'rank', 'homepage_url', 'category_groups_list',
            'num_funding_rounds', 'total_funding_usd', 'employee_count',
            'logo_url', 'country', 'last_funding_round'
        ]]
        startup_info = seriesToDict(startup_row)
        startup_list[num] = startup_info
    return startup_list


if __name__ == '__main__':
    app.run(debug=True)