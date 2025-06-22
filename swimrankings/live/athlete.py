from .enums import Gender


class Athlete:
    def __init__(
        self,
        meet,
        gender,
        first_name,
        nation,
        yob,
        name_prefix,
        last_name,
        full_name,
        id,
        swimrankings_id,
        club_id,
    ):
        self.meet = meet
        self.gender = gender
        self.first_name = first_name
        self.nation = nation
        self.yob = yob
        self.name_prefix = name_prefix
        self.last_name = last_name
        self.full_name = full_name
        self.id = id
        self.swimrankings_id = swimrankings_id
        self.club_id = club_id
        self.club = None

    def get_club(self):
        if self.meet.clubs is None:
            self.meet.fetch()
        return self.meet.clubs[self.club_id]

    def fetch(self):
        self.club = self.get_club()

    @classmethod
    def parse(cls, meet, data):
        return cls(
            meet,
            Gender(int(data.get("gender", 0))),
            data.get("firstname"),
            data.get("nation"),
            int(data.get("yob", -1)),
            data.get("nameprefix"),
            data.get("lastname"),
            data.get("fullname"),
            int(data["id"]),
            int(data.get("swrid", -1)),
            int(data.get("clubid", -1)),
        )

    def __repr__(self):
        return f"<Athlete ({self.full_name})>"


class AthleteList:
    def __init__(self, athletes):
        self.athletes = {a.id: a for a in athletes}

    def __getitem__(self, id):
        return self.athletes[id]

    def __iter__(self):
        return iter(self.athletes.values())

    def by_name(self, name):
        for athlete in self:
            if athlete.full_name == name:
                return athlete
        raise KeyError(name)

    def __repr__(self):
        return f"<AthleteList ({len(self.athletes)} athletes)>"
