class Subject:
    def __init__(self, id: str, teacherId: str, disciplineId: str):
        self.id = id
        self.teacherId = teacherId
        self.disciplineId = disciplineId

    def to_dict(self):
        return {
            "id": self.id,
            "teacherId": self.teacherId,
            "disciplineId": self.disciplineId
        }