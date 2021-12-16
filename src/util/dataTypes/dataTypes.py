from typing import List

def parseInts(string, default=1) -> int:
    if (falsey(string)): return default
    else: return int(string, 10)

def parseLists(string, default=[], delimiter=",") -> List:
    if (falsey(string)): return default
    else: return string.split(delimiter)

def replaceBool(string, valTrue: any, valFalse: any):
    if (truthy(string)): return valTrue
    else: return valFalse

def truthy(val) -> bool:
    if bool(val): return True 
    else: return False

def falsey(val) -> bool:
    if not bool(val): return True
    else: return False
