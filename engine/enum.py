from enum import IntEnum, Enum

class Side(IntEnum):
    FACEUP   = 1
    FACEDOWN = 0

class TraitType(IntEnum):
    MAIN  = 0
    SHORT = 1

class AreaTextType(IntEnum):
    NAME = 0
    EFFECT = 1

class StartIndex(IntEnum):
    EVOLUTION = 0
    AREA = 200

class EndIndex(IntEnum):
    EVOLUTION = 99
    AREA = 400

class DeckType(IntEnum):
    EVOLUTION = 0
    AREA = 1

class ItemType(str, Enum):
    GREEN = 'grn'
    RED   = 'red'
    BLUE  = 'blu'

