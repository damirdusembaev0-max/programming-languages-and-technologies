"""Система учета заявок на общежитие (мини-проект СРО, тема 20).

Модули: валидация -> модель данных -> бизнес-логика -> хранилище -> консольный интерфейс.
"""
import json
import os
import re
from dataclasses import dataclass, field, asdict
from datetime import date
from enum import Enum


class Status(str, Enum):
    NEW = "Новая"
    REVIEW = "На рассмотрении"
    APPROVED = "Одобрена"
    REJECTED = "Отклонена"


# Допустимые переходы статусов (жизненный цикл заявки)
TRANSITIONS = {
    Status.NEW: {Status.REVIEW, Status.REJECTED},
    Status.REVIEW: {Status.APPROVED, Status.REJECTED},
    Status.APPROVED: set(),
    Status.REJECTED: set(),
}

FACULTIES = ("ИТ", "Экономика", "Инженерия", "Право", "Педагогика")
SORT_KEYS = ("id", "fio", "course", "date", "status")
LETTERS = "A-Za-zА-Яа-яЁёӘәІіҢңҒғҮүҰұҚқӨөҺһ"
WORD = "[%s]+(?:-[%s]+)*" % (LETTERS, LETTERS)  # дефис только между буквами


class ValidationError(ValueError):
    """Ошибка проверки введенных данных."""


@dataclass
class Application:
    id: int
    fio: str
    student_id: str
    faculty: str
    course: int
    phone: str
    reason: str
    created: str
    status: Status = Status.NEW
    history: list = field(default_factory=list)


# ---------- Валидация ----------
def validate_fio(fio):
    fio = " ".join(fio.split())
    if not re.fullmatch("%s( %s){1,2}" % (WORD, WORD), fio):
        raise ValidationError("ФИО: 2-3 слова, только буквы (например, Иванов Иван)")
    return fio


def validate_phone(phone):
    digits = re.sub(r"[\s\-()]", "", phone)
    if not re.fullmatch(r"(\+7|8)[0-9]{10}", digits):
        raise ValidationError("Телефон: формат +7XXXXXXXXXX или 8XXXXXXXXXX")
    return "+7" + digits[-10:]


def validate_student_id(sid):
    sid = sid.strip()
    if not re.fullmatch(r"[0-9]{6,8}", sid):
        raise ValidationError("Номер студ. билета: 6-8 цифр")
    return sid


def validate_course(course):
    if isinstance(course, bool):
        raise ValidationError("Курс должен быть целым числом")
    try:
        c = int(course)
    except (TypeError, ValueError):
        raise ValidationError("Курс должен быть целым числом")
    if not 1 <= c <= 6:
        raise ValidationError("Курс: число от 1 до 6")
    return c


def validate_faculty(faculty):
    faculty = faculty.strip()
    if faculty not in FACULTIES:
        raise ValidationError("Факультет: " + ", ".join(FACULTIES))
    return faculty


def validate_reason(reason):
    reason = reason.strip()
    if len(reason) < 5:
        raise ValidationError("Причина: минимум 5 символов")
    if len(reason) > 200:
        raise ValidationError("Причина: максимум 200 символов")
    return reason


# ---------- Бизнес-логика ----------
class DormRegistry:
    def __init__(self, path=None):
        self.path = path
        self.items = []
        if path and os.path.exists(path):
            self.load()

    def _next_id(self):
        return max((a.id for a in self.items), default=0) + 1

    def add(self, fio, student_id, faculty, course, phone, reason):
        fio = validate_fio(fio)
        student_id = validate_student_id(student_id)
        faculty = validate_faculty(faculty)
        course = validate_course(course)
        phone = validate_phone(phone)
        reason = validate_reason(reason)
        for a in self.items:  # одна активная заявка на студента
            if a.student_id == student_id and a.status in (Status.NEW, Status.REVIEW):
                raise ValidationError("У студента уже есть активная заявка №%d" % a.id)
        app = Application(self._next_id(), fio, student_id, faculty, course,
                          phone, reason, date.today().isoformat())
        app.history.append("%s: создана (%s)" % (app.created, app.status.value))
        self.items.append(app)
        return app

    def get(self, app_id):
        for a in self.items:
            if a.id == app_id:
                return a
        raise KeyError("Заявка №%s не найдена" % app_id)

    def change_status(self, app_id, new_status):
        app = self.get(app_id)
        if new_status not in TRANSITIONS[app.status]:
            raise ValidationError("Переход «%s» -> «%s» недопустим"
                                  % (app.status.value, new_status.value))
        app.history.append("%s: %s -> %s" % (date.today().isoformat(),
                                             app.status.value, new_status.value))
        app.status = new_status
        return app

    def search(self, query="", status=None, faculty=None):
        q = query.strip().lower()
        result = []
        for a in self.items:
            if q and q not in a.fio.lower() and q not in a.student_id:
                continue
            if status and a.status != status:
                continue
            if faculty and a.faculty != faculty:
                continue
            result.append(a)
        return result

    def sort(self, items, key="id", reverse=False):
        if key not in SORT_KEYS:
            raise ValidationError("Ключ сортировки: " + ", ".join(SORT_KEYS))
        getter = {"id": lambda a: a.id, "fio": lambda a: a.fio.lower(),
                  "course": lambda a: a.course, "date": lambda a: (a.created, a.id),
                  "status": lambda a: list(Status).index(a.status)}[key]
        return sorted(items, key=getter, reverse=reverse)

    def stats(self):
        counts = {s: 0 for s in Status}
        for a in self.items:
            counts[a.status] += 1
        return counts

    def delete(self, app_id):
        self.items.remove(self.get(app_id))

    # ---------- Хранилище ----------
    def save(self):
        if not self.path:
            return
        data = [dict(asdict(a), status=a.status.value) for a in self.items]
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        with open(self.path, encoding="utf-8") as f:
            for d in json.load(f):
                d["status"] = Status(d["status"])
                self.items.append(Application(**d))


# ---------- Консольный интерфейс ----------
def print_table(items):
    if not items:
        print("Заявок нет.")
        return
    print("%-4s %-26s %-9s %-11s %-3s %-16s %-10s" %
          ("№", "ФИО", "Билет", "Факультет", "Кс", "Статус", "Дата"))
    print("-" * 85)
    for a in items:
        print("%-4d %-26s %-9s %-11s %-3d %-16s %-10s" %
              (a.id, a.fio[:26], a.student_id, a.faculty, a.course, a.status.value, a.created))


def ask(prompt, validator):
    while True:  # цикл повторного ввода до корректного значения
        try:
            return validator(input(prompt))
        except ValidationError as e:
            print("  Ошибка:", e)


def choose_status():
    for i, s in enumerate(Status, 1):
        print("  %d - %s" % (i, s.value))
    try:
        return list(Status)[int(input("Статус: ")) - 1]
    except (ValueError, IndexError):
        raise ValidationError("Выберите номер из списка")


MENU = """
=== Заявки на общежитие ===
1. Подать заявку        5. Статистика
2. Список заявок        6. Удалить заявку
3. Поиск / фильтр       7. История заявки
4. Сменить статус       0. Выход
"""


def main(path="applications.json"):
    reg = DormRegistry(path)
    while True:
        print(MENU)
        try:
            cmd = input("Выбор: ").strip()
            if cmd == "1":
                fio = ask("ФИО: ", validate_fio)
                sid = ask("№ студ. билета: ", validate_student_id)
                fac = ask("Факультет (%s): " % ", ".join(FACULTIES), validate_faculty)
                crs = ask("Курс (1-6): ", validate_course)
                ph = ask("Телефон: ", validate_phone)
                rs = ask("Причина: ", validate_reason)
                a = reg.add(fio, sid, fac, crs, ph, rs)
                print("Заявка №%d принята." % a.id)
            elif cmd == "2":
                key = input("Сортировать по (%s) [id]: " % ", ".join(SORT_KEYS)).strip() or "id"
                print_table(reg.sort(reg.items, key))
            elif cmd == "3":
                q = input("Имя или № билета (Enter - пропустить): ")
                st = input("Фильтр по статусу? (y/n): ").strip().lower() == "y"
                st = choose_status() if st else None
                print_table(reg.search(q, st))
            elif cmd == "4":
                app_id = int(input("№ заявки: "))
                a = reg.change_status(app_id, choose_status())
                print("Статус заявки №%d: %s" % (a.id, a.status.value))
            elif cmd == "5":
                for s, n in reg.stats().items():
                    print("%-16s %d" % (s.value, n))
                print("Всего:", len(reg.items))
            elif cmd == "6":
                reg.delete(int(input("№ заявки: ")))
                print("Удалено.")
            elif cmd == "7":
                for line in reg.get(int(input("№ заявки: "))).history:
                    print(" ", line)
            elif cmd == "0":
                reg.save()
                print("Данные сохранены. До свидания!")
                break
            else:
                print("Неизвестная команда.")
            reg.save()
        except ValueError as e:
            print("Ошибка:", e if isinstance(e, ValidationError) else "введите число")
        except KeyError as e:
            print("Ошибка:", e.args[0])
        except (EOFError, KeyboardInterrupt):
            reg.save()
            print("\nВвод прерван. Данные сохранены.")
            break


if __name__ == "__main__":
    main()
