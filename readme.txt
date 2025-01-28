# HTTP Health Checker
Checks HTTP endpoints from YAML file and returns the percentage of successful checks per domain every 15 seconds. A successful request is defined by a 2xx status code and <500ms response time

# Prereqs
python3
pip3

# Installation
```bash
pip3 install -r requirements.txt
```

# Usage
```bash
python3 healthcheck.py endpoints.yaml
```

The yaml file must have the following schema:
name (string, required)
url (string, required)
method (string, optional)
headers (dictionary, optional) 
body (string, optional)