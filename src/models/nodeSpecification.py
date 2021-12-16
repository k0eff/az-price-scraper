from typing import Dict, List


class NodeSpecification():
    mincpu: int = None
    maxcpu: int = None
    minram: int
    maxram: int
    os: str
    spot: str
    excluded: List

    def __init__(self, params) -> None:
        for k, v in params.items():
            if k == "mincpu": v = self.parseInts(v, 1)
            elif k == "maxcpu": v = self.parseInts(v, 32)
            elif k == "minram": v = self.parseInts(v, 1)
            elif k == "maxram": v = self.parseInts(v, 32)
            elif k == "excluded": v = self.parseLists(v)
            elif k == "spot": v = self.replaceBool(v, "lowpriority", "")
            setattr(self, k, v)
        return

    def asdict(self): 
        return {
            "mincpu": self.mincpu,
            "maxcpu": self.maxcpu,
            "minram": self.minram,
            "maxram": self.maxram,
            "os": self.os,
            "spot": self.spot,
            "excluded": self.excluded
        }


    def parseInts(self, string, default=1) -> int:
        if (self.falsey(string)): return default
        else: return int(string, 10)

    def parseLists(self, string, default=[], delimiter=",") -> List:
        if (self.falsey(string)): return default
        else: return string.split(delimiter)

    def replaceBool(self, string, valTrue, valFalse):
        if (self.truthy(string)): return valTrue
        else: return valFalse

    def truthy(self, val):
        if bool(val): return True 
        else: return False

    def falsey(self, val):
        if not bool(val): return True
        else: return False