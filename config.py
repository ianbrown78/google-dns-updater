import logging
import os
import os.path
from dotenv import load_dotenv
from pathlib import Path


class config():
    if os.path.isfile('.env'):
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)

    def __init__(self):
        logging.info("Starting configuration.")
        self.ttl = os.environ.get('ttl', 3600)

        self.app = os.environ.get('app', '"app" variable has not been set.')

        self.functionName = os.environ.get('FUNCTION_NAME', '')
        self.gcpRegion = os.environ.get('FUNCTION_REGION', '')
        self.gcpProject = os.environ.get('project', '"project" variable has not been set.')
        self.gcpAuthKeyJsonFile = os.environ.get('authKeyJsonFile', '')
        self.gcpDnsZoneName = os.environ.get('dnsZoneName', '"dnsZoneName" variable has not been set.')
        self.gcpDnsDomain = os.environ.get('dnsDomain', '"dnsDomain" variable has not been set.')


cfg = config()
