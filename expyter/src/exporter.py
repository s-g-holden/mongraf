from prometheus_client import start_http_server, Summary, Info
import random
import time
import os
from atlassian import Bamboo

BAMBOO_URL = os.environ.get("BAMBOO_URL", "http://localhost:8085")
ATLASSIAN_USER = os.environ.get("ATLASSIAN_USER", "bamboo")
ATLASSIAN_PASSWORD = os.environ.get("ATLASSIAN_PASSWORD", "password")

bamboo = Bamboo(url=BAMBOO_URL, username=ATLASSIAN_USER, password=ATLASSIAN_PASSWORD)

PLAN_INFO = Info('bamboo_plan_info', 'General plan information.')

def plan_info_request(key):
    """Request plan info."""
    PLAN_INFO.info(bamboo.get_plan(key))

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        plan_info_request('EX-EX')