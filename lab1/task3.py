try:
    n = int(input("Введите число: "))
    print(n % 10 * 100 + n // 10 % 10 * 10 + n // 100)
except ValueError:
    print("Ошибка: Вы ввели не число!")
