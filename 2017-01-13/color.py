from pyplasm import *
from fpformat import *

def color(r,g,b):
    """This function return a rgb Color"""
    return [float(fix(r/255.,6)),float(fix(g/255.,6)),float(fix(b/255.,6)),1.000000]