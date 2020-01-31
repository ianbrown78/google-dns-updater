import logging
import os
from dotenv import load_dotenv
from pathlib import Path

logger = logging.getLogger('root')

class config():
  env_path = Path('.') / '.env'
  load_dotenv(dotenv_path=env_path)

  def __init__(self):
    self.ttl = os.getenv("ttl", 3600)
    
    self.app = os.getenv("app", "")

    self.gcpProject = os.getenv("project", "")
    self.gcpAuthKeyJsonFile = os.getenv("authKeyJsonFile", "")
    self.gcpDnsZoneName = os.getenv("dnsZoneName", "")
    self.gcpDnsDomain = os.getenv("dnsDomain", "")
    
cfg = config()
