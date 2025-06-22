from .enums import Gender, Course
from swimrankings.util.sorter import Sorter
from swimrankings.util.time_parser import Time


class Result:
    def __init__(
        self,
        meet,
        event,
        gender,
        nation,
        medal,
        heat_info,
        club_text,
        club_name,
        club_code,
        athlete_id,
        splits,
        entry_time,
        points,
        id,
        age_text,
        heat_id,
        swimrankings_id,
        lane,
        swim_time,
        info,
        club_id,
        entry_course,
        name_text,
        place,
        dsq_reason,
    ):
        self.meet = meet
        self.event = event
        self.gender = gender
        self.nation = nation
        self.medal = medal
        self.heat_info = heat_info
        self.club_text = club_text
        self.club_name = club_name
        self.club_code = club_code
        self.athlete_id = athlete_id
        self.splits = splits
        self.entry_time = entry_time
        self.points = points
        self.id = id
        self.age_text = age_text
        self.heat_id = heat_id
        self.swimrankings_id = swimrankings_id
        self.lane = lane
        self.swim_time = swim_time
        self.info = info
        self.club_id = club_id
        self.entry_course = entry_course
        self.name_text = name_text
        self.place = place
        self.dsq_reason = dsq_reason
        self.athlete = None
        self.club = None

    @classmethod
    def parse(cls, meet, event, data):
        return cls(
            meet,
            event,
            Gender(int(data.get("gender", 0))),
            data.get("nation"),
            int(data.get("medal", -1)),
            data.get("heatinfo"),
            data.get("clubtext"),
            data.get("clubname"),
            data.get("clubcode"),
            int(data.get("athleteid", -1)),
            data.get("splits"),
            Time(data.get("entrytime", "00.00")),
            int(data.get("points", 0)),
            int(data["id"]),
            data.get("agetext"),
            int(data.get("heatid", -1)),
            int(data.get("swrid", -1)),
            int(data.get("lane", -1)),
            Time(data.get("swimtime", "00.00")),
            data.get("info"),
            data.get("clubid"),
            Course(int(data.get("entrycourse", 0))),
            data.get("nametext"),
            int(data.get("place", -1)),
            data.get("commentdsq"),
        )

    def get_athlete(self):
        if self.meet.athletes is None:
            self.meet.fetch()
        return self.meet.athletes[self.athlete_id]

    def get_club(self):
        if self.meet.clubs is None:
            self.meet.fetch()
        return self.meet.clubs[self.club_id]

    def fetch(self):
        self.athlete = self.get_athlete()
        self.club = self.get_club()

    def __repr__(self):
        return f"<Result ({self.place if self.dsq_reason is None else 'DSQ'}. {self.name_text} {self.swim_time.string})>"


class AgeGroupResults:
    def __init__(self, meet, event, age_group_id, results, numbered):
        self.meet = meet
        self.event = event
        self.age_group_id = age_group_id
        self.results = results
        self.numbered = numbered
        self.age_group = None

    def __getitem__(self, id):
        return self.results[id]

    def get_age_group(self):
        if self.age_group_id == -1:
            return None
        if self.meet.age_groups is None:
            self.meet.fetch()
        return self.meet.age_groups[self.age_group_id]

    def fetch(self):
        self.age_group = self.get_age_group()

    def __repr__(self):
        return f"<AgeGroupResults ({len(self.results)} results)>"

    @classmethod
    def parse(cls, meet, event, data):
        sorter = Sorter(lambda a: a.swim_time)
        results = {}
        for r in data["results"]:
            result = Result.parse(meet, event, r)
            results[result.id] = result
            sorter.feed(result)
        numbered = sorter.extract()
        return cls(meet, event, int(data.get("id", -1)), results, numbered)


class ResultList:
    def __init__(self, meet, event, age_groups):
        self.meet = meet
        self.event = event
        self.age_groups = age_groups

    def __getitem__(self, index):
        return self.age_groups[index]

    def by_id(self, id):
        for i in self.age_groups:
            if id in i.results:
                return i.results[id]
        raise KeyError

    @classmethod
    def parse(cls, meet, event, data):
        age_groups = []
        for a in data["agegroups"]:
            age_group_results = AgeGroupResults.parse(meet, event, a)
            age_groups.append(age_group_results)
        return cls(meet, event, age_groups)

    def __repr__(self):
        return f"<ResultList ({len(self.age_groups)} age groups)>"
