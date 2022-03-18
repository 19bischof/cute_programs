from icecream import ic
from enum import Enum,auto
class Oath(Enum):
    name = "What kind of oath"
    Marriage = auto()
    Army = auto()
    Court = auto()
    President = auto()
    Promise = auto()
    lawyer = auto()
    doctor = auto()

ic(Oath.name)
ic(Oath.mro())
ic(Oath.register())