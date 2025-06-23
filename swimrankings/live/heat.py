from .entry import Entry
from .enums import Status
from swimrankings.util.sorter import Sorter
import datetime


class Heat:
    def __init__(self, meet, event, status, id, entries, time, code):
        self.status = status
        self.id = id
        self.entries = entries
        self.time = time
        self.code = code
        self.meet = meet
        self.event = event

    @classmethod
    def parse(cls, meet, event, data):
        return cls(
            meet,
            event,
            Status(data["status"]),
            int(data["id"]),
            [Entry.parse(meet, event, i) for i in data.get("entries", [])],
            datetime.time.fromisoformat(data.get("time") or "00:00"),
            int(data.get("code", -1)),
        )


class HeatList:
    def __init__(self, meet, event, heats, numbered):
        self.heats = heats
        self.numbered = numbered

    def __getitem__(self, id):
        return self.heats[id]

    @classmethod
    def parse(cls, meet, event, data):
        sorter = Sorter(lambda a: a.code)
        heats = {}
        for h in data["heats"]:
            heat = Heat.parse(meet, event, h)
            heats[heat.id] = heat
            sorter.feed(heat)
        numbered = sorter.extract()
        return cls(meet, event, heats, numbered)
