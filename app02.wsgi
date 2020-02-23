#!/usr/bin/python3
import sys
sys.path.insert(0,"/var/www/app02/")
sys.path.insert(0,"/var/www/app02/app02/")

import logging
logging.basicConfig(stream=sys.stderr)

from app02 import app as application