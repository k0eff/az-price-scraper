from typing import Dict, List

from src.util.dataTypes.dataTypes import parseInts, parseLists, replaceBool

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
            if k == "mincpu": v = parseInts(v, 1)
            elif k == "maxcpu": v = parseInts(v, 32)
            elif k == "minram": v = parseInts(v, 1)
            elif k == "maxram": v = parseInts(v, 32)
            elif k == "excluded": v = parseLists(v)
            elif k == "spot": v = replaceBool(v, "lowpriority", "")
            setattr(self, k, v)
        return

    def asdict(self) -> Dict: 
        return {
            "mincpu": self.mincpu,
            "maxcpu": self.maxcpu,
            "minram": self.minram,
            "maxram": self.maxram,
            "os": self.os,
            "spot": self.spot,
            "excluded": self.excluded
        }


