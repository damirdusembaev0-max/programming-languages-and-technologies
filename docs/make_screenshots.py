"""Запускает реальное приложение со сценарным вводом и рисует консольные скриншоты в screenshots/."""
import builtins, contextlib, io, os, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
import dorm  # noqa: E402

FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)


def run(inputs, path):
    """Выполняет main() с готовым вводом; ввод эхом выводится как в терминале."""
    it = iter(inputs)
    buf = io.StringIO()
    old = builtins.input

    def fake(prompt=""):
        v = next(it)
        buf.write(prompt + v + "\n")
        return v
    builtins.input = fake
    try:
        with contextlib.redirect_stdout(buf):
            dorm.main(path)
    finally:
        builtins.input = old
    return buf.getvalue()


def render(text, name, skip_menu_repeats=True):
    lines = text.rstrip("\n").split("\n")
    w, lh = 900, 22
    img = Image.new("RGB", (w, lh * len(lines) + 56), "#1e1e1e")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 32], fill="#3a3a3a")
    d.text((14, 6), "python src/dorm.py", font=FONT, fill="#dddddd")
    for i, ln in enumerate(lines):
        col = "#ff7b72" if "Ошибка" in ln else ("#7ee787" if "принята" in ln or "Статус заявки" in ln else "#e6e6e6")
        d.text((14, 44 + i * lh), ln, font=FONT, fill=col)
    out = os.path.join(ROOT, "screenshots", name)
    img.save(out)
    print("saved", name, img.size)


def strip_menu(t):  # оставляем меню один раз, убираем повторы
    menu = dorm.MENU
    first = t.find(menu) + len(menu)
    return t[:first] + t[first:].replace(menu, "\n")


tmp = tempfile.mkdtemp()
db = os.path.join(tmp, "db.json")
# 1. Подача заявки с ошибками ввода (повторный запрос)
t1 = run(["1", "Иван", "Иванов Иван", "12", "250123", "ИТ", "9", "2", "12345", "87011234567",
          "abc", "Проживаю в другом городе", "0"], db)
render(strip_menu(t1), "01_podacha_zayavki.png")
# 2. Несколько заявок + список с сортировкой
more = [("Сериков Алихан", "250124", "Экономика", "1", "+77021112233", "Иногородний студент"),
        ("Ахметова Дана", "250125", "ИТ", "3", "+77759998877", "Семья проживает в другой области")]
inp = []
for m in more:
    inp += ["1", *m]
inp += ["2", "fio", "0"]
t2 = run(inp, db)
render(strip_menu(t2), "02_spisok_sortirovka.png")
# 3. Смена статуса, недопустимый переход, поиск
t3 = run(["4", "1", "2", "4", "1", "3", "4", "1", "3", "3", "ахмет", "n", "0"], db)
render(strip_menu(t3), "03_status_poisk.png")
# 4. Статистика и история
t4 = run(["5", "7", "1", "0"], db)
render(strip_menu(t4), "04_statistika_istoriya.png")
