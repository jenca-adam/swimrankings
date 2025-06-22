class Club:
    def __init__(self, meet, nation, short_name, region, long_code, id, code, name):
        self.meet = meet
        self.nation = nation
        self.short_name = short_name
        self.region = region
        self.long_code = long_code
        self.id = id
        self.code = code
        self.name = name

    @classmethod
    def parse(cls, meet, data):
        return cls(
            meet,
            data.get("nation"),
            data.get("shortname"),
            data.get("region"),
            data.get("longcode"),
            int(data.get("id")),
            data.get("code"),
            data.get("name"),
        )

    def __repr__(self):
        return f"<Club ({self.code})>"


class ClubList:
    def __init__(self, clubs):
        self.clubs = {club.id: club for club in clubs}

    def __getitem__(self, id):
        return self.clubs[id]

    def by_id(self, id):
        return self[id]

    def by_code(self, code):
        for i in self:
            if i.code == code:
                return i
        raise KeyError(code)

    def __iter__(self):
        return iter(self.clubs.values())

    def __repr__(self):
        return f"<ClubList ({len(self.clubs)} clubs)>"
