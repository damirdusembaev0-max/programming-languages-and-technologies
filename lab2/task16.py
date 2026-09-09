a = float(input("Введите сторону a: "))
b = float(input("Введите сторону b: "))
c = float(input("Введите сторону c: "))

perimeter = a + b + c
semi_perimeter = perimeter / 2
area = (semi_perimeter * (semi_perimeter - a) * (semi_perimeter - b) * (semi_perimeter - c)) ** 0.5

print("Периметр:", perimeter)
print("Полупериметр:", semi_perimeter)
print("Площадь:", area)
