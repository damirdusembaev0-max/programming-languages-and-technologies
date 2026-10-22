try:
    gradus = float(input("Введите температуру °C:" ))
    print(gradus * 1.8 + 32, "°F")
    print(gradus + 273.15,"K")
except ValueError:
    print("Ошибка: Вы ввели не число!")
