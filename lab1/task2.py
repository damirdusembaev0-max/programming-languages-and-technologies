try:
    sec = int(input("Введите кол-во секунд: "))
    hours = sec // 3600
    minutes = (sec % 3600) // 60
    seconds = sec - (hours * 3600) - (minutes * 60)
    print(hours,"ч", minutes,"м", seconds,"с")
except ValueError:
    print("Ошибка: Вы ввели не число!")
