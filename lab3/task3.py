class Student:
    def __init__(self, name: str, age: int, specialty: str):
        self.name = name
        self.age = age
        self.specialty = specialty

    def display_info(self):
        """Метод 1: Вывод информации о студенте"""
        print(f"Студент: {self.name} | Возраст: {self.age} | Специальность: {self.specialty}")

    def change_specialty(self, new_specialty: str):
        """Метод 2: Изменение специальности"""
        print(f"--> {self.name} переведен на специальность: {new_specialty}")
        self.specialty = new_specialty

    def celebrate_birthday(self):
        """Метод 3: Увеличение возраста (день рождения)"""
        self.age += 1
        print(f"🎉 У {self.name} день рождения! Теперь ему/ей {self.age} лет.")

# Тест-сценарий
s1 = Student("Адиль", 19, "ВТПО")
s2 = Student("Алина", 20, "Маркетинг")
s3 = Student("Руслан", 18, "Data Science")

s1.display_info()
s1.change_specialty("Архитектура")
s3.celebrate_birthday()