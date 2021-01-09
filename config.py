import logging
import os
import os.path
from dotenv import load_dotenv
from pathlib import Path

class config():
  if (os.path.isfile('.env')):
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

  def __init__(self):
    logging.info("Starting configuration.")
    self.ttl = os.getenv("ttl", 3600)
    
    self.app = os.getenv("app", "")

    self.functionName = os.getenv("FUNCTION_NAME", "")
    self.gcpRegion = os.getenv("FUNCTION_REGION", "")
    self.gcpProject = os.getenv("project", "")
    self.gcpAuthKeyJsonFile = os.getenv("authKeyJsonFile", "")
    self.gcpDnsZoneName = os.getenv("dnsZoneName", "")
    self.gcpDnsDomain = os.getenv("dnsDomain", "")
    
cfg = config()
