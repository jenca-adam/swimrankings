import enum


class Gender(enum.IntEnum):
    MEN = 1
    WOMEN = 2
    MIXED = 3
    BOYS = 11
    GIRLS = 12
    UNKNOWN = 0

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class Stroke(enum.IntEnum):
    FREE = 1
    BACK = 2
    BREAST = 3
    FLY = 4
    MEDLEY = 5
    UNKNOWN = 0

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class Course(enum.IntEnum):
    LONG = 1
    SHORT = 2
    UNKNOWN = 0

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class Status(enum.IntEnum):
    PLANNED = 1
    # PLANNED = 2
    # no idea what 2 is
    ONGOING = 3
    FINISHED = 5
    UNKNOWN = 0

    @classmethod
    def _missing_(cls, value):
        if value == 2:
            return cls.PLANNED
        return cls.UNKNOWN


class ResultStatus(enum.IntEnum):
    OK = 1
    DSQ = 2
    DNS = 3
    DNF = 4
    UNKNOWN = 0

    @classmethod
    def _missing(cls, value):
        return cls.UNKNOWN
