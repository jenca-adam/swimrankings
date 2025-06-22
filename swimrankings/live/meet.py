import datetime
import requests
import time
from dataclasses import dataclass
from .club import Club, ClubList
from .athlete import Athlete, AthleteList
from .event import EventList
from .session import SessionList
from .age_group import AgeGroupList
from .enums import Course, Status


@dataclass
class MeetStats:
    relays: int = 0
    entries: int = 0
    athletes: int = 0
    clubs: int = 0


class MeetInfo:
    def __init__(
        self,
        stats,
        user_info,
        has_messages,
        points,
        lanes,
        point_scores,
        days,
        is_multi_course,
    ):
        self.stats = stats
        self.user_info = user_info
        self.has_messages = has_messages
        self.points = points
        self.lanes = lanes
        self.point_scores = point_scores
        self.days = days
        self.is_multi_course = is_multi_course

    @classmethod
    def parse(cls, data):
        return cls(
            MeetStats(**data.get("statistic", {})),
            data.get("userinfo"),
            data.get("hasmessages", False),
            data.get("points"),
            (data.get("lanemin", 0), data.get("lanemax", 0)),
            data.get("pointscores"),
            data.get("days", 0),
            data.get("is_multi_course", False),
        )


class Meet:
    def __init__(
        self,
        id,
        city,
        name,
        nation,
        number,
        course,
        end_date,
        start_date,
        status,
        last_update,
        build_number,
    ):
        self.id = id
        self.city = city
        self.name = name
        self.nation = nation
        self.number = number
        self.course = course
        self.end_date = end_date
        self.start_date = start_date
        self.status = status
        self.last_update = last_update
        self.build_number = build_number
        self.info = None
        self.clubs = None
        self.athletes = None
        self.events = None
        self.sessions = None
        self.age_groups = None

    @classmethod
    def parse(cls, data):
        return cls(
            int(data["id"]),
            data.get("city"),
            data.get("name"),
            data.get("nation"),
            data.get("number"),
            Course(data.get("course", 1)),
            datetime.date.fromisoformat(data["enddate"]),
            datetime.date.fromisoformat(data["startdate"]),
            Status(data.get("status")),
            datetime.datetime.fromisoformat(data["lastupdate"]),
            data.get("buildnr"),
        )

    def make_request(self, path, params={}):
        p = {"t": int(time.time() * 1000)}
        p.update(params)
        return requests.get(f"https://live.swimrankings.net/meets/{self.id}/{path}")

    def get_info(self):
        response = self.make_request("main.json")
        if response.ok:
            return MeetInfo.parse(response.json())

    def get_clubs(self):
        response = self.make_request("clubs.json")
        if response.ok:
            return ClubList([Club.parse(self, i) for i in response.json()])

    def get_athletes(self):
        response = self.make_request("athletes.json")
        if response.ok:
            return AthleteList([Athlete.parse(self, i) for i in response.json()])

    def get_events(self):
        response = self.make_request("events.json")
        if response.ok:
            return EventList.parse(self, response.json())

    def get_sessions(self):
        response = self.make_request("eventsBySession.json")
        if response.ok:
            return SessionList.parse(self, response.json())

    def get_age_groups(self):
        response = self.make_request("agegroups.json")
        if response.ok:
            return AgeGroupList.parse(response.json())

    def fetch(self):
        self.info = self.get_info()
        self.clubs = self.get_clubs()
        self.athletes = self.get_athletes()
        self.events = self.get_events()
        self.sessions = self.get_sessions()
        self.age_groups = self.get_age_groups()

    def __repr__(self):
        return f"<Meet (name={self.name}, city={self.city}, nation={self.nation}, course={self.course!r})>"


class MeetGroup:
    def __init__(self, code, name, meets):
        self.code = code
        self.name = name
        self.meets = meets

    @classmethod
    def parse(cls, data):
        return cls(
            data.get("code"),
            data.get("name"),
            [Meet.parse(i) for i in data.get("meets", [])],
        )

    def __getitem__(self, i):
        return self.meets[i]

    def __repr__(self):
        return f"<MeetGroup (code={self.code}, name={self.name}) ({len(self.meets)} meets)>"


class MeetList:
    def __init__(self, groups):
        self.groups = groups

    def get_group(self, /, code=None, name=None):
        for group in self.groups:
            if code and group.code == code or name and group.name == name:
                return group

    def __getitem__(self, code):
        return self.get_group(code=code)

    @classmethod
    def parse(cls, data):
        return cls([MeetGroup.parse(i) for i in data.get("meetgroups", [])])

    def __repr__(self):
        return f"<MeetList ({len(self.groups)} groups)>"


def get_meet_list():
    response = requests.get(
        "https://live.swimrankings.net/index.php",
        params={"Cmd": "Meets", "t": int(time.time() * 1000)},
    )
    if response.ok:
        data = response.json()
        if data.get("status") == "OK":
            return MeetList.parse(data)
