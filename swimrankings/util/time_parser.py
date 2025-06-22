import re

time_regex = re.compile(r"(\d+:)?(\d{1,2}:)?(\d{2}\.\d{2})")  # H:MM:SS.SS


def to_float(num):
    try:
        return float(num.lstrip("0").rstrip(":"))
    except (AttributeError, ValueError):
        return 0.0


class Time:
    def __init__(self, string):
        match = time_regex.search(string)
        if not match:
            raise ValueError(f"invalid time string: {string}")
        groups = match.groups()
        if (
            groups[1] is None and groups[0] is not None
        ):  # if hours are not present the second group is not matched
            self.mins, self.hours, self.secs = map(to_float, groups)
        else:
            self.hours, self.mins, self.secs = map(to_float, groups)
        self.string = string

    @property
    def _tup(self):
        return (self.hours, self.mins, self.secs)

    def __eq__(self, other):
        return isinstance(other, Time) and other._tup == self._tup

    def __gt__(self, other):
        return isinstance(other, Time) and self._tup > other._tup

    def __ge__(self, other):
        return isinstance(other, Time) and self._tup >= other._tup

    def __repr__(self):
        return f"Time(hours={self.hours}, mins={self.mins}, secs={self.secs})"
