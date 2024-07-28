from enum import IntEnum

class Side(IntEnum):
    FACEUP   = 1
    FACEDOWN = 0

class TraitType(IntEnum):
    MAIN  = 0
    SHORT = 1

class AreaTextType(IntEnum):
    NAME = 0
    EFFECT = 1
