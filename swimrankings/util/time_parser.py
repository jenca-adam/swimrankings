import re
from dataclasses import dataclass

time_regex = re.compile(r"(\d+:)?(\d{1,2}:)?(\d{2}\.\d{2})")  # H:MM:SS.SS
split_regex = re.compile(r"(\S+)\s*\(\s*(\S+)\s*\)")


def to_float(num):
    try:
        return float(num.lstrip("0").rstrip(":"))
    except (AttributeError, ValueError):
        return 0.0


class Time:
    def __init__(self, string):
        match = time_regex.search(string)
        if not match:
            self.invalid = True
            self.hours, self.mins, self.secs = -1, -1, -1
        else:
            groups = match.groups()
            if (
                groups[1] is None and groups[0] is not None
            ):  # if hours are not present the second group is not matched
                self.mins, self.hours, self.secs = map(to_float, groups)
            else:
                self.hours, self.mins, self.secs = map(to_float, groups)
            self.invalid = False
        self.string = string

    @property
    def _tup(self):
        return (self.hours, self.mins, self.secs)

    def __eq__(self, other):
        if self.invalid:
            return False
        return isinstance(other, Time) and other._tup == self._tup

    def __gt__(self, other):
        if self.invalid:
            return True
        if other.invalid:
            return False
        return isinstance(other, Time) and self._tup > other._tup

    def __ge__(self, other):
        if self.invalid:
            return True
        if other.invalid:
            return False
        return isinstance(other, Time) and self._tup >= other._tup

    def __repr__(self):
        return f"Time(hours={self.hours}, mins={self.mins}, secs={self.secs})"


@dataclass
class Split:
    total: Time
    last: Time


class Splits:
    def __init__(self, splits):
        self.splits = {
            k: (
                Split(*(Time(i.strip()) for i in split_regex.search(v).groups()))
                if split_regex.match(v)
                else None
            )
            for k, v in splits.items()
        }
