class GroupStudent:
    """Вспомогательный класс студента для хранения личных данных"""
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

class Group:
    """Основной класс для управления списком студентов"""
    def __init__(self, group_name: str):
        self.group_name = group_name
        self.__students = []  # Скрытый список студентов внутри группы

    def add_student(self, student: GroupStudent):
        """Метод 1: Добавление студента в группу"""
        self.__students.append(student)
        print(f"➕ Студент {student.name} добавлен в группу {self.group_name}")

    def remove_student(self, student_name: str):
        """Метод 2: Удаление студента по имени"""
        for student in self.__students:
            if student.name == student_name:
                self.__students.remove(student)
                print(f"➖ Студент {student_name} удален из группы {self.group_name}")
                return
        print(f"❓ Студент {student_name} не найден в группе {self.group_name}")

    def get_average_age(self) -> float:
        """Метод 3: Подсчет среднего возраста студентов в группе"""
        if not self.__students:
            return 0.0
        total_age = sum(student.age for student in self.__students)
        return round(total_age / len(self.__students), 1)

    def display_group(self):
        """Метод 4: Вывод всего состава группы"""
        print(f"\n👥 Состав группы {self.group_name} (Средний возраст: {self.get_average_age()}):")
        if not self.__students:
            print("   Группа пуста.")
        for student in self.__students:
            print(f"   - {student.name}, {student.age} лет")

# Тест-сценарий (Создание 3 объектов-групп и студентов)
group_it = Group("ИС-24")
group_eco = Group("ЭК-23")
group_math = Group("МАТ-25")

# Создаем студентов
st1 = GroupStudent("Медет", 19)
st2 = GroupStudent("Айша", 21)
st3 = GroupStudent("Кирилл", 20)

# Проверка сценариев
group_it.add_student(st1)
group_it.add_student(st2)
group_it.add_student(st3)
group_it.display_group()

group_it.remove_student("Айша")
group_it.display_group()