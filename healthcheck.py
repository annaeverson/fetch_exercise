import yaml
import requests
import time
import sys
from urllib.parse import urlparse

# Check for blank input
if len(sys.argv) == 1:
    print("Input file name")
    exit()

yaml_file = open(sys.argv[1], 'r')
endpoints = yaml.safe_load(yaml_file)
health_checks = {}

# Set the domain for each endpoint for easier lookup later
# Add unique domains to the health check dictionary
for endpoint in endpoints:
    endpoint['domain'] = urlparse(endpoint['url']).netloc
    if endpoint['domain'] not in health_checks:
        health_checks[endpoint['domain']] = {'ups':0, 'total':0}

# Format and execute HTTP request and check for 'up' criteria
def isUp(endpoint):
    headers = endpoint.get('headers', '')
    method = endpoint.get('method', 'GET')
    body = endpoint.get('body', '')
    if method == 'POST':
        response = requests.post(endpoint['url'], headers=headers, data=body)
    elif method == 'PUT':
        response = requests.put(endpoint['url'], headers=headers, data=body)
    elif method == 'PATCH':
        response = requests.patch(endpoint['url'], headers=headers, data=body)
    elif method == 'DELETE':
        response = requests.delete(endpoint['url'], headers=headers, data=body)
    elif method == "GET":
        response = requests.get(endpoint['url'], headers=headers, data=body)
    if 200 <= response.status_code <= 299 and response.elapsed.total_seconds()<0.5:
        return True
    return False

starttime = time.monotonic()
while True:
    # Check each endpoint and add results to healthcheck dictionary
    for endpoint in endpoints:
        health_checks[endpoint['domain']]['total'] +=1
        if isUp(endpoint):
            health_checks[endpoint['domain']]['ups'] += 1
    print()
    for key,value in health_checks.items():
        percentage = round((value['ups']/value['total'])*100)
        print(f'{key} has {percentage}% availability percentage')
    time.sleep(15.0 - ((time.monotonic() - starttime) % 15.0))