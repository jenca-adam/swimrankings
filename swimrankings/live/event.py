import datetime

from .enums import Stroke, Gender
from .entry import EntryList
from .result import ResultList
from .heat import HeatList
from swimrankings.util.sorter import Sorter


class Event:
    def __init__(
        self,
        meet,
        gender,
        stroke,
        age_group,
        is_relay,
        distance,
        id,
        age_groups,
        number,
        time,
        date,
        round,
    ):
        self.meet = meet
        self.gender = gender
        self.stroke = stroke
        self.age_group = age_group
        self.is_relay = is_relay
        self.distance = distance
        self.id = id
        self._age_groups = age_groups
        self.number = number
        self.time = time
        self.date = date
        self.round = round
        self.age_groups = None
        self.entries = None
        self.results = None
        self.heats = None

    def get_age_groups(self):
        if self.meet.age_groups is None:
            self.meet.fetch()
        return [self.meet.age_groups[int(id)] for id in self._age_groups]

    def get_entries(self):
        response = self.meet.make_request(f"entries/{self.id}.json")
        if response.ok:
            return EntryList.parse(self.meet, self, response.json()["entries"])

    def get_heats(self):
        response = self.meet.make_request(f"heats/{self.id}.json")
        if response.ok:
            return HeatList.parse(self.meet, self, response.json())

    def get_results(self):
        response = self.meet.make_request(f"results/{self.id}.json")
        if response.ok:
            return ResultList.parse(self.meet, self, response.json())

    def fetch(self):
        self.age_groups = self.get_age_groups()
        self.entries = self.get_entries()
        self.results = self.get_results()
        self.heats = self.get_heats()

    @classmethod
    def parse(cls, meet, data):
        return cls(
            meet,
            Gender(int(data.get("gender", 0))),
            Stroke(int(data.get("stroke", 0))),
            data.get("agegroup", {}),
            data.get("isrelay", False),
            data.get("distance"),
            int(data["id"]),
            data.get("agegroups", []),
            int(data.get("number", 0)),
            datetime.time.fromisoformat(data.get("time") or "00:00"),
            datetime.date.fromisoformat(data.get("date") or "1970-1-1"),
            int(data.get("round", 0)),
        )

    def __repr__(self):
        return f"<Event (distance={self.distance}, stroke={self.stroke!r}, gender={self.gender!r})>"


class EventList:
    def __init__(self, meet, events, numbered):
        self.events = events
        self.meet = meet
        self.numbered = numbered

    def __getitem__(self, id):
        return self.events[id]

    @classmethod
    def parse(cls, meet, data):
        events = {}
        sorter = Sorter(lambda event: event.number)
        for key, value in data.items():
            if key.isdigit():
                event = Event.parse(meet, value)
                events[int(key)] = event
                if event.number > 0:
                    sorter.feed(event)
        numbered = sorter.extract()
        return cls(meet, events, numbered)

    def __repr__(self):
        return f"<EventList ({len(self.events)} events)>"
