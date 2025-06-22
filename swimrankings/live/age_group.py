class AgeGroup:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def parse(cls, data):
        return cls(int(data["id"]), data.get("name"))

    def __repr__(self):
        return f"<AgeGroup {self.name}>"


class AgeGroupList:
    def __init__(self, age_groups):
        self.age_groups = age_groups

    def __getitem__(self, id):
        return self.age_groups[id]

    @classmethod
    def parse(cls, data):
        age_groups = {}
        for key, value in data.items():
            if key.isdigit():
                age_groups[int(key)] = AgeGroup.parse(value)
        return cls(age_groups)

    def __repr__(self):
        return f"<AgeGroupList ({len(self.age_groups)} age groups)>"
