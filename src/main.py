# The main python file that does the work
from google.cloud import dns
import config
import time

def main():
  cfg = config.cfg
  client = dns.Client(project=cfg.gcpProject)
  zone = client.zone(cfg.gcpZoneName, cfg.gcpDnsDomain)

  # Get the records in batches
  records, page_token = zone.list_resource_record_sets()
  while page_token is not None:
    next_batch, page_token = zone.list_resource_record_sets(
      page_token=page_token)  # API request
    records.extend(next_batch)

  # create an update
  record_set = zone.resource_record_set(
    'www.example.com.', 'CNAME', TWO_HOURS, ['www1.example.com.',])
  changes = zone.changes()
  changes.add_record_set(record_set)
  changes.create()  # API request
  while changes.status != 'done':
    print('Waiting for changes to complete')
    time.sleep(60)     # or whatever interval is appropriate
    changes.reload()   # API request
