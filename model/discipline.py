class Discipline:
    def __init__(self, id: str, name: str, hours: int, pre_requisite: str):
        self.id = id
        self.name = name
        self.hours = hours
        self.pre_requisite = pre_requisite
        
    def to_dict(self):
        return {
            "id": self.id,
            "name" : self.name,
            "hours": self.hours,
            "pre_requisite": self.pre_requisite
        }