import sys
import os

sys.path.append(os.path.dirname(__file__))


from constants import *
from requests_utils import *
from bs_utils import *
from excel_utils import *
from files_utils import *

def isType(obj, value):
    return obj.type == value