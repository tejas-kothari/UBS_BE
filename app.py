import time
import re
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
    page = int(request.args.get('page'))
    rowsPerPage = int(request.args.get('rowsPerPage'))
    search = request.args.get('search')
    filterCategory = request.args.get('filterCategory')
    filterCountry = request.args.get('filterCountry')
    filterPhase = request.args.get('filterPhase')
    filterSize = request.args.get('filterSize')

    startup_list = startups.copy()[[
        'uuid', 'name', 'rank', 'homepage_url', 'category_groups_list',
        'num_funding_rounds', 'total_funding_usd', 'employee_count',
        'logo_url', 'country', 'last_funding_round'
    ]]

    if filterSize:
        startup_list = startup_list[startup_list['employee_count'] ==
                                    filterSize]
    if filterPhase:
        startup_list = startup_list[startup_list['last_funding_round'] ==
                                    filterPhase]
    if filterCountry:
        startup_list = startup_list[startup_list['country'] == filterCountry]
    if filterCategory:
        startup_list = startup_list[
            startup_list['category_groups_list'].str.contains(filterCategory)]
    if search:
        startup_list = startup_list[startup_list['name'].str.contains(
            search, flags=re.IGNORECASE)]

    totalNumFilteredStartups = len(startup_list)
    startup_payload = {'totalNumStartups': totalNumFilteredStartups}

    if totalNumFilteredStartups > rowsPerPage:
        startup_list = startup_list[rowsPerPage * (page - 1):rowsPerPage *
                                    page]
    startup_payload['filteredStartups'] = dfToDict(startup_list)

    return startup_payload


if __name__ == '__main__':
    app.run(debug=True)