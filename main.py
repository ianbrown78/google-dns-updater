# The main python file that does the work
import google.cloud.logging
import logging
import time

import google.auth
from google.cloud import dns
from google.oauth2 import service_account

import config

# app = flask.Flask(__name__)
# app.config["DEBUG"] = True

# Grab our configuration
cfg = config.cfg

# Configure the client & zone
if len(cfg.gcpAuthKeyJsonFile) == 0:
    credentials, project = google.auth.default()
else:
    credentials = service_account.Credentials.from_service_account_file(cfg.gcpAuthKeyJsonFile)

log_client = google.cloud.logging.Client()
log_client.get_default_handler()
log_client.setup_logging()

client = dns.Client(project=cfg.gcpProject, credentials=credentials)
zone = client.zone(cfg.gcpDnsZoneName, cfg.gcpDnsDomain)

records = ""
changes = zone.changes()


def page_not_found(e):
    logging.error("The resource could not be found. %s", e)
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


def page_unauthorized(e):
    logging.error("You are not authorized to access this resource. %s", e)
    return "<h1>401</h1><p>You are not authorized to access this resource.</p>", 401


def main(request):
    a_record_found = False
    aaaa_record_found = False
    a_record_changed = False
    aaaa_record_changed = False
    ret_val = ""
    
    logging.info("Update request started.")

    request_args = request.get_json(silent=True)
    
    # Assign our parameters
    if request_args:
        host = request_args['host']
        ipv4 = request_args['ipv4']
        ipv6 = request_args['ipv6']
        key = request_args['key']

    # Check we have the required parameters
    if not (host and key and (ipv4 or ipv6)):
        return page_not_found(404)

    # Check the key
    if not (check_key(key)):
        return page_unauthorized(401)

    # Get a list of the current records
    records = get_records()
	

    # Check for matching records
    for record in records:
        if record.name == host and record.record_type == 'A' and ipv4:
            for data in record.rrdatas:
                if test_for_record_change(data, ipv4):
                    add_to_change_set(record, 'delete')
                    add_to_change_set(create_record_set(host, record.record_type, ipv4), 'create')
                    a_record_changed = True
                    ret_val = "IPv4 changed successful.\n"
                else:
                    ret_val = "IPv4 record up to date.\n"
        if record.name == host and record.record_type == 'AAAA' and ipv6:
            for data in record.rrdatas:
                if test_for_record_change(data, ipv6):
                    add_to_change_set(record, 'delete')
                    add_to_change_set(create_record_set(host, record.record_type, ipv6), 'create')
                    aaaa_record_changed = True
                    ret_val += "IPv6 changed successful.\n"
                else:
                    ret_val += "IPv6 Record up to date.\n"

    if not (a_record_found or aaaa_record_found):
        ret_val = "No matching records.\n"

    if a_record_changed or aaaa_record_changed:
        execute_change_set(changes)

    return ret_val


def check_key(key):
    if cfg.app == key:
        logging.info("Key received from client is correct.")
        return True
    else:
        logging.error("Key received from client is incorrect.")
        return False


def get_records(client=client, zone=zone):
    # Get the records in batches
    return zone.list_resource_record_sets(max_results=100, page_token=None, client=client)


def test_for_record_change(old_ip, new_ip):
    logging.info("Existing IP is {}".format(old_ip))
    logging.info("New IP is {}".format(new_ip))
    if old_ip != new_ip:
        logging.info("IP addresses do no match. Update required.")
        return True
    else:
        logging.info("IP addresses match. No update required.")
        return False


def create_record_set(host, record_type, ip):
    record_set = zone.resource_record_set(
        host, record_type, cfg.ttl, [ip])
    return record_set


def add_to_change_set(record_set, atype):
    if atype == 'delete':
        return changes.delete_record_set(record_set)
    else:
        return changes.add_record_set(record_set)


def execute_change_set(changes):
    logging.info("Change set executed")
    changes.create()
    while changes.status != 'done':
        logging.info("Waiting for changes to complete. Change status is {}".format(changes.status))
        time.sleep(20)
        changes.reload()

# app.run()
