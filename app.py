import time
from flask import Flask, request
import pandas as pd

organizations = pd.read_csv('csv/organizations.csv')
print("done reading csv")

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/get_organization_info')
def get_organization():
    org_uuid = request.get_json()['org_uuid']
    organization_row = organizations.loc[organizations['uuid'] == org_uuid]

    organization_info = {}
    for column in organization_row.columns:
        organization_info[column] = organization_row[column].iloc[0]
    
    return organization_info

app.run(debug=True)