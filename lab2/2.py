"""
Напишите программу, которая заданное вещественное число выводит в формате с плавающей точкой в нормализованной форме. Например:
Введите число: 0.0012
Формат плавающей точки: x = 1.2 * 10 ** -3
Введите число: 25.073
Формат плавающей точки: x = 2.5073 * 10 ** 1
"""

from decimal import Decimal
origValue = Decimal(input("Введите число: "))
count = 0
value = abs(origValue)
if value < 1:
    while (value < 1):
        value *= 10
        count -= 1
elif value > 10:
    while (value > 10):
        value /= 10
        count += 1
if origValue < 0:
    origValue = -value
else:
    origValue = value
print("Формат плавающей точки: x =", origValue, "* 10 **", count)
