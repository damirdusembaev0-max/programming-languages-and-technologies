
class Course:
    def __init__(self, name, teacher):
        self.name = name
        self.teacher = teacher
        self.stud = []

    def add_stud(self, new):
        self.stud.append(new)

    def show(self):
        print(f" Группа: {self.name}\n", f"Преподаватель: {self.teacher}\n", "Студенты:")
        for i in self.stud:
            print(f"- {i}")

result = Course("IS25-22", "Rashidinov D.R.")
result.add_stud("Miras")
result.add_stud("Diyar")
result.add_stud("Grigoriy")
result.show()