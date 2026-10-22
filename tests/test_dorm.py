"""Автотесты. Docstring теста: «сценарий || ожидаемый результат» (используется в протоколе)."""
import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from dorm import (DormRegistry, Status, ValidationError, validate_course,  # noqa: E402
                  validate_fio, validate_student_id)

OK = dict(fio="Иванов Иван", student_id="250123", faculty="ИТ", course=1,
          phone="+77011234567", reason="Проживаю в другом городе")


def make(**over):
    d = dict(OK)
    d.update(over)
    return d


class TestDorm(unittest.TestCase):
    def setUp(self):
        self.r = DormRegistry()

    # ---------- основные сценарии ----------
    def test_T01_add_application(self):
        """Добавить корректную заявку || Заявка в списке, id=1, статус «Новая»"""
        a = self.r.add(**OK)
        self.assertEqual((a.id, a.status, len(self.r.items)), (1, Status.NEW, 1))

    def test_T02_status_workflow(self):
        """Новая → На рассмотрении → Одобрена || Статус «Одобрена», 3 записи истории"""
        a = self.r.add(**OK)
        self.r.change_status(a.id, Status.REVIEW)
        self.r.change_status(a.id, Status.APPROVED)
        self.assertEqual(a.status, Status.APPROVED)
        self.assertEqual(len(a.history), 3)

    def test_T03_search_and_filter(self):
        """Поиск по ФИО, по номеру билета, фильтр по факультету || Находится ровно 1 заявка в каждом случае"""
        self.r.add(**OK)
        self.r.add(**make(fio="Петров Пётр", student_id="250124", faculty="Право"))
        self.assertEqual(len(self.r.search("петров")), 1)
        self.assertEqual(len(self.r.search("250123")), 1)
        self.assertEqual(len(self.r.search(faculty="Право")), 1)

    def test_T04_sort(self):
        """Сортировка по ФИО и по курсу (убывание) || ФИО: Агаев, Иванов; курсы: 3, 1"""
        self.r.add(**OK)
        self.r.add(**make(fio="Агаев Али", student_id="250124", course=3))
        self.assertEqual([a.fio for a in self.r.sort(self.r.items, "fio")],
                         ["Агаев Али", "Иванов Иван"])
        self.assertEqual([a.course for a in self.r.sort(self.r.items, "course", True)], [3, 1])

    def test_T05_save_load_stats(self):
        """Сохранение в JSON, загрузка, статистика || Данные восстановлены, «Новая» = 1"""
        self.r.add(**OK)
        self.r.path = os.path.join(tempfile.mkdtemp(), "db.json")
        self.r.save()
        r2 = DormRegistry(self.r.path)
        self.assertEqual(r2.items[0].fio, "Иванов Иван")
        self.assertEqual(r2.stats()[Status.NEW], 1)

    # ---------- ошибочный ввод ----------
    def test_T06_empty_fio(self):
        """Пустое ФИО || ValidationError, заявка не создана"""
        with self.assertRaises(ValidationError):
            self.r.add(**make(fio="   "))
        self.assertEqual(self.r.items, [])

    def test_T07_bad_phone(self):
        """Телефон «12345» || ValidationError"""
        with self.assertRaises(ValidationError):
            self.r.add(**make(phone="12345"))

    def test_T08_bad_transition(self):
        """Переход Новая → Одобрена минуя рассмотрение || ValidationError, статус не изменился"""
        a = self.r.add(**OK)
        with self.assertRaises(ValidationError):
            self.r.change_status(a.id, Status.APPROVED)
        self.assertEqual(a.status, Status.NEW)

    def test_T09_duplicate_active(self):
        """Вторая активная заявка того же студента || ValidationError"""
        self.r.add(**OK)
        with self.assertRaises(ValidationError):
            self.r.add(**OK)

    # ---------- граничные случаи ----------
    def test_T10_course_bounds(self):
        """Курс 1 и 6 принимаются, 0 и 7 нет || Границы 1..6 соблюдены"""
        self.r.add(**make(course=1))
        self.r.add(**make(student_id="250124", course=6))
        for bad in (0, 7):
            with self.assertRaises(ValidationError):
                self.r.add(**make(student_id="250125", course=bad))

    def test_T11_reason_bounds(self):
        """Причина 5 и 200 символов принимается, 4 и 201 нет || Границы 5..200 соблюдены"""
        self.r.add(**make(reason="a" * 5))
        self.r.add(**make(student_id="250124", reason="a" * 200))
        for n, sid in ((4, "250125"), (201, "250126")):
            with self.assertRaises(ValidationError):
                self.r.add(**make(student_id=sid, reason="a" * n))

    def test_T12_empty_registry(self):
        """Пустой реестр: поиск, статистика, get(1) || [], нули, KeyError"""
        self.assertEqual(self.r.search("x"), [])
        self.assertEqual(sum(self.r.stats().values()), 0)
        with self.assertRaises(KeyError):
            self.r.get(1)

    # ---------- регрессия: дефекты, найденные при исследовательском тестировании ----------
    def test_T13_fio_hyphens_only(self):
        """ФИО из одних дефисов «- -» и «-Иван- Иванов» (дефект D1) || ValidationError; «Иванов-Петров Иван» принимается"""
        for bad in ("- -", "-Иван- Иванов"):
            with self.assertRaises(ValidationError):
                validate_fio(bad)
        self.assertEqual(validate_fio("Иванов-Петров Иван"), "Иванов-Петров Иван")

    def test_T14_non_ascii_digits(self):
        """Номер билета арабскими цифрами «٢٥٠١٢٣» (дефект D2) || ValidationError"""
        with self.assertRaises(ValidationError):
            validate_student_id("٢٥٠١٢٣")

    def test_T15_bool_course(self):
        """Курс True (дефект D3) || ValidationError"""
        with self.assertRaises(ValidationError):
            validate_course(True)

    def test_T16_eof_input(self):
        """Конец ввода (Ctrl+D) в меню (дефект D4) || Программа сохраняет данные и завершается без traceback"""
        import builtins
        import dorm
        path = os.path.join(tempfile.mkdtemp(), "db.json")
        old = builtins.input

        def raise_eof(_=""):
            raise EOFError
        builtins.input = raise_eof
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                dorm.main(path)
        finally:
            builtins.input = old


if __name__ == "__main__":
    unittest.main(verbosity=2)
