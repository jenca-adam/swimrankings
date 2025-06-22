from .enums import Course, Status
from swimrankings.util.sorter import Sorter
import datetime


class Session:
    def __init__(self, meet, day, events, lanes, id, course, number, time, name, date):
        self.meet = meet
        self.day = day
        self._events = events
        self.lanes = lanes
        self.id = id
        self.course = course
        self.number = number
        self.time = time
        self.name = name
        self.date = date
        self.events = None

    def get_events(self):
        if self.meet.events is None:
            self.meet.fetch()
        return [
            (Status(int(ev["status"])), self.meet.events[int(ev["id"])])
            for ev in self._events
        ]

    def fetch(self):
        self.events = self.get_events()

    @classmethod
    def parse(cls, meet, data):
        return cls(
            meet,
            int(data.get("day", 0)),
            data["events"],
            (int(data.get("lanemin", 0)), int(data.get("lanemax", 0))),
            int(data["id"]),
            Course(int(data.get("course", 0))),
            int(data.get("number", 0)),
            datetime.time.fromisoformat(data.get("time", "00:00")),
            data.get("name"),
            datetime.date.fromisoformat(data.get("date", "1970-01-01")),
        )

    def __repr__(self):
        return f"<Session ({self.number})>"


class SessionList:
    def __init__(self, meet, sessions, numbered):
        self.sessions = sessions
        self.numbered = numbered
        self.meet = meet

    def __getitem__(self, id):
        return self.sessions[id]

    @classmethod
    def parse(cls, meet, data):
        sorter = Sorter(lambda session: session.number)
        sessions = {}
        for s in data["sessions"]:
            session = Session.parse(meet, s)
            sessions[session.id] = session
            if session.number > 0:
                sorter.feed(session)
        numbered = sorter.extract()
        return cls(meet, sessions, numbered)

    def __repr__(self):
        return f"<SessionList ({len(self.sessions)} sessions)>"
