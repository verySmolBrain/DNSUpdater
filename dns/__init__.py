import sys 

from .config import *
from .domain_request import *
from .setup import *
from .error_handler import *

def version():
    return "0.0.0.1"

def config_version():
    return "0.1"

def path():
    return sys.path