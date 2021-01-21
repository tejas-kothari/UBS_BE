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
    investors = funding_df['investors']
    funding_df = funding_df.drop('investors', axis=1)

    funding_info = dfToDict(funding_df)
    for index, investor in investors.items():
        if not pd.isnull(investor):
            funding_info[index]['investor'] = ast.literal_eval(investor)
        else:
            funding_info[index]['investor'] = ""

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