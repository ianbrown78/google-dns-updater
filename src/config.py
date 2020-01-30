import logging
import os
import string
from distutils import util

logger = logging.getLogger('root')

class config():
  def __init__(self):
    self.app = os.getenv("app", "")

    self.gcpProject = os.getenv("project", "")
    self.gcpAuthKeyJsonFile = os.getenv("authKeyJsonFile", "")
    self.gcpDnsZoneName = os.getenv("dnsZoneName", "")
    self.gcpDnsDomain = os.getenv("dnsDomain", "")
    
cfg = config() 
