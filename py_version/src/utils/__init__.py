import sys
import os

sys.path.append(os.path.dirname(__file__))


from bs_utils import *
from requests_utils import *
from constants import *



def isType(obj, value):
    return obj.type == value