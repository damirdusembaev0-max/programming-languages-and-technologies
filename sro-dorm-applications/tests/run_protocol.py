"""Запускает тесты и формирует протокол tests/protocol.md (ID | сценарий | ожидаемо | фактически | статус)."""
import io
import os
import platform
import sys
import unittest
from datetime import date

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import test_dorm  # noqa: E402

suite = unittest.defaultTestLoader.loadTestsFromModule(test_dorm)
tests = [t for case in suite for t in case]  # список до запуска (раннер очищает suite)
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
bad = {t.id().split(".")[-1]: msg for t, msg in result.failures + result.errors}
rows = []
for t in tests:
    name = t._testMethodName
    scen, exp = (t._testMethodDoc or "").split("||")
    tid = "T-" + name.split("_")[1][1:]
    ok = name not in bad
    actual = exp.strip() if ok else "Расхождение: " + bad[name].strip().splitlines()[-1]
    rows.append("| %s | %s | %s | %s | %s |" % (tid, scen.strip(), exp.strip(), actual, "PASS" if ok else "FAIL"))
head = ("Дата: %s. Окружение: Python %s, %s.\nКоманда: `python tests/run_protocol.py`\n\n"
        "| ID | Сценарий | Ожидаемо | Фактически | Статус |\n|---|---|---|---|---|\n"
        % (date.today().strftime("%d.%m.%Y"), platform.python_version(), platform.system()))
total = "\n\nИтого: %d из %d PASS.\n" % (result.testsRun - len(bad), result.testsRun)
with open(os.path.join(here, "protocol.md"), "w", encoding="utf-8") as f:
    f.write(head + "\n".join(rows) + total)
print(head + "\n".join(rows) + total)
sys.exit(0 if result.wasSuccessful() else 1)
