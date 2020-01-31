# The main python file that does the work
from google.cloud import dns
from google.oauth2 import service_account
import google.auth
import config
import time
import sys, urllib
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Grab our configuration
cfg = config.cfg

# Configure the client & zone
if (len(cfg.gcpAuthKeyJsonFile) == 0):
  credentials, project = google.auth.default()
else:
  credentials = service_account.Credentials.from_service_account_file(cfg.gcpAuthKeyJsonFile)
client = dns.Client(project=cfg.gcpProject, credentials=credentials)
zone = client.zone(cfg.gcpDnsZoneName, cfg.gcpDnsDomain)

records = ""
changes = zone.changes()

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/', methods=['POST'])
def main(request):
  query_parameters = request.args
  
  # Assign our parameters
  host = query_parameters.get('host')
  ip = query_parameters.get('ip')
  key = query_parameters.get('key')

  # Check we have the required parameters
  if not (host and ip and key):
    return page_not_found(404)

  # Check the key
  if not (check_key(key)):
    return page_not_found(404)

  # Get a list of the current records
  records = get_records()
  
  # Check for matching records
  for record in records:
    if (host == record.name):
      for data in record.rrdatas:
        if (test_for_record_change(data, ip)):
          add_to_change_set(record, 'delete')
          add_to_change_set(create_record_set(host, record.record_type, ip), 'create')
          execute_change_set(changes)
          return "Change successful."
        else:
          return "Record up to date."
  
  return "No matching records."

def check_key(key):
  if (cfg.app == key):
    return True
  else:
    return False

def get_records(client=client, zone=zone):
  # Get the records in batches
  return zone.list_resource_record_sets(max_results=100, page_token=None, client=client)

def test_for_record_change(old_ip, new_ip):
  if (old_ip != new_ip):
    return True
  else:
    return False

def create_record_set(host, record_type, ip):
  record_set = zone.resource_record_set(
    host, record_type, cfg.ttl, [ip])
  return record_set  

def add_to_change_set(record_set, atype):
  if (atype == 'delete'):
    return changes.delete_record_set(record_set)
  else:
    return changes.add_record_set(record_set)

def execute_change_set(changes):
  changes.create()
  while changes.status != 'done':
    print('Waiting for changes to complete')
    time.sleep(20)
    changes.reload()

app.run()
