from typing import Set

class Teacher:
    def __init__(self, id: str, name: str, disciplines: Set[str]):
        self.id = id
        self.name = name
        self.disciplines = disciplines
        
    def to_dict(self):
        return {
            "id": self.id,
            "name" : self.name,
            "disciplines": self.disciplines
        }