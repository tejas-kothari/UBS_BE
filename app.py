import time
from flask import Flask, request
from flask_cors import CORS
import pandas as pd
from parser import seriesToDict
from random import randrange

print("reading csv...")
startups = pd.read_csv("csv/hitech_startups.csv")
print("done reading csv")

app = Flask(__name__)
CORS(app, origins=[r'http://localhost:.*', r'^https:\/\/temg4952a-team1-.*.web\.app'])


@app.route("/time")
def get_current_time():
    return {"time": time.time()}


@app.route("/get_startup")
def get_startup():
    uuid = request.get_json()["uuid"]
    startup_row = startups[startups["uuid"] == uuid].iloc[0]
    startup_info = seriesToDict(startup_row)
    return startup_info


@app.route("/get_startup_list")
def get_startup_list():
    startup_list = {}
    for num in range(0, 50):
        index = randrange(0, len(startups))
        startup_row = startups.iloc[index][[
            'uuid', 'name', 'rank', 'homepage_url', 'category_groups_list',
            'total_funding_usd', 'employee_count', 'logo_url', 'country'
        ]]
        startup_info = seriesToDict(startup_row)
        startup_list[num] = startup_info
    return startup_list


if __name__ == '__main__':
    app.run()