from prometheus_client import start_http_server, Summary
import random
import time
from atlassian import Bamboo

BAMBOO_URL = os.environ.get("BAMBOO_URL", "http://localhost:8085")
ATLASSIAN_USER = os.environ.get("ATLASSIAN_USER", "admin")
ATLASSIAN_PASSWORD = os.environ.get("ATLASSIAN_PASSWORD", "admin")

bamboo = Bamboo(url=BAMBOO_URL, username=ATLASSIAN_USER, password=ATLASSIAN_PASSWORD)

agent_status = bamboo.agent_status()
print(agent_status)

activity = bamboo.activity()
print(activity)

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request(random.random())
