import requests
from requests.auth  import HTTPBasicAuth
import subprocess
import time
import json
import csv
import math

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def convert_to_csv(plan_key, csv_name, keys, list_to_convert):
    with open('csvs/' + plan_key + '_' + csv_name, 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys, extrasaction='ignore')
        dict_writer.writeheader()
        dict_writer.writerows(list_to_convert)

def get_auth():
    with open('user-tfs.json') as user_file:
        user_info = json.load(user_file)
        if 'PAT' in user_info:
            return BearerAuth(user_info['PAT'])
        return HTTPBasicAuth(user_info['username'], user_info['password'])

def send_request(url, auth):
    if 'http://' in url:
        url = 'https://' + url.split('http://')[1]
    return requests.get(url,
                        auth=auth,
                        headers={'Accept': 'application/json'}
                    ).json()

def gather_data(build_key, no_of_builds):
    request_count = math.ceil(no_of_builds / 25)
    plans = []
    for i in range(0, request_count):
        data = send_request('https://devops.innovateuk.org/build-management/rest/api/latest/result/' + build_key + '?expand=results.result.stages.stage.results.result&&start-index=' + str(25 * i), auth)
        plans.extend(data['results']['result'])
        if int(data['results']['size']) < 25:
            return plans
    return plans[0:no_of_builds]
    

build_keys = ['UFS-MONOAMBUILD', 'UFS-MONOADMBUILD', 'UFS-MONOUIBUILD', 'UFS-MONOOMBUILD', 'UFS-GDSCOMP']
auth = get_auth()
found_keys = set()
jobs = {}
for build_key in build_keys:
    # data = send_request('https://devops.innovateuk.org/build-management/rest/api/latest/result/' + build_key + '?expand=results.result.stages.stage.results.result', auth)
    # plans = data['results']['result']
    plans = gather_data(build_key, 100)
    convert_to_csv(build_key, 'MainBuilds.csv', ['buildResultKey', 'buildState', 'buildStartedTime', 'buildCompletedTime', 'buildDurationInSeconds', 'buildDurationDescription', 'successfulTestCount', 'failedTestCount', 'skippedTestCount', ], plans)

    # jobs = {}
    for plan in plans:
        for stage in plan['stages']['stage']:
            for job in stage['results']['result']:
                if job['planName'] not in jobs:
                    jobs[job['planName']] = []
                job['stageName'] = stage['name']
                jobs[job['planName']].append(job)

    for plan_name, job in jobs.items():
        convert_to_csv(build_key, 'job_' + plan_name + '.csv', ['planName', 'stageName', 'buildResultKey', 'buildState', 'buildStartedTime', 'buildCompletedTime', 'queueTimeInSeconds', 'buildDurationInSeconds', 'buildDurationDescription', 'successfulTestCount', 'failedTestCount', 'skippedTestCount'], job)
joblists = jobs.values()
all_jobs = [item for sublist in joblists for item in sublist]
convert_to_csv('allPlans2_', 'jobs.csv', ['planName', 'stageName',  'buildResultKey', 'buildState', 'buildStartedTime', 'buildCompletedTime', 'queueTimeInSeconds', 'buildDurationInSeconds', 'buildDurationDescription', 'successfulTestCount', 'failedTestCount', 'skippedTestCount'], all_jobs)