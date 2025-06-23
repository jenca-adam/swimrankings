from .enums import Gender, Course
from swimrankings.util.sorter import Sorter
from swimrankings.util.time_parser import Time


class Entry:
    def __init__(
        self,
        meet,
        event,
        gender,
        nation,
        club_text,
        club_code,
        athlete_id,
        entry_time,
        id,
        age_text,
        club_id,
        course,
        name_text,
        place,
        lane,
    ):
        self.meet = meet
        self.event = event
        self.gender = gender
        self.nation = nation
        self.club_text = club_text
        self.club_code = club_code
        self.athlete_id = athlete_id
        self.entry_time = entry_time
        self.id = id
        self.age_text = age_text
        self.club_id = club_id
        self.course = course
        self.name_text = name_text
        self.place = place
        self.lane = lane
        self.club = None
        self.athlete = None

    def get_club(self):
        if self.meet.clubs is None:
            self.meet.fetch()
        return self.meet.clubs[self.club_id]

    def get_athlete(self):
        if self.meet.athletes is None:
            self.meet.fetch()
        return self.meet.athletes[self.athlete_id]

    def fetch(self):
        self.club = self.get_club()
        self.athlete = self.get_athlete()

    @classmethod
    def parse(cls, meet, event, data):
        return cls(
            meet,
            event,
            Gender(int(data.get("gender", 0))),
            data.get("nation"),
            data.get("clubtext"),
            data.get("clubcode"),
            int(data.get("athleteid", -1)),
            Time(data.get("entrytime")),
            data["id"],
            data.get("agetext"),
            int(data.get("clubid", -1)),
            Course(int(data.get("entrycourse", 0))),
            data.get("nametext"),
            int(data.get("place", -1)),
            int(data.get("lane", -1)),
        )

    def __repr__(self):
        return f"<Entry ({self.name_text}, {self.entry_time.string})>"


class EntryList:
    def __init__(self, meet, event, entries, numbered):
        self.meet = meet
        self.event = event
        self.entries = entries
        self.numbered = numbered

    def __getitem__(self, id):
        return self.entries[id]

    @classmethod
    def parse(cls, meet, event, data):
        entries = {}
        sorter = Sorter(lambda a: a.entry_time)
        for e in data:
            entry = Entry.parse(meet, event, e)
            entries[entry.id] = entry

            sorter.feed(entry)
        numbered = sorter.extract()
        return cls(meet, event, entries, numbered)

    def __repr__(self):
        return f"<EntryList ({len(self.entries)} entries)>"
