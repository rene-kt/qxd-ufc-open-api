class Discipline:
    def __init__(self, code: str, name: str, hours: int, pre_requisite: str):
        self.code = code
        self.name = name
        self.hours = hours
        self.pre_requisite = pre_requisite
        
    def to_dict(self):
        return {
            "code": self.code,
            "name" : self.name,
            "hours": self.hours,
            "pre_requisite": self.pre_requisite
        }