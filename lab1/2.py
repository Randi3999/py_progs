"""
Напишите программу решения квадратного уравнения по трем коэффициентам, учитывая, что в нем могут быть нулевые коэффициенты (в том числе, все три). Считать, что, если все три коэффициента нулевые, то уравнение имеет бесконечное множество решений. 
"""
from math import sqrt
a = int(input("Напишите коэфициент a: "))
b = int(input("Напишите коэфициент b: "))
c = int(input("Напишите коэфициент c: "))

if a == 0 and b == 0 and c == 0:
    print("Бесконечное число решений")
    exit()
elif a == 0 and b == 0:
    print("Решения нет")
    exit()
elif a == 0 and c == 0:
    print ("x: ", 0)
    exit()
elif b == 0 and c == 0:
    print("x: ", 0)
    exit()

if a == 0:
    print ("x: ", -c / b)
    exit()
elif b == 0 and c == -1:
    print("Решения нет")
    exit()
elif b == 0:
    print("x1: ", sqrt(-c / a), "x2: ", -sqrt(-c / a))
    exit()
elif c == 0:
    print("x1: ", 0,"x2: ", -b / a)
    exit()

discriminant = (b ** 2) - (4 * a * c)

if sqrt(discriminant) > 0:
    x1 = (-b + sqrt(discriminant)) / (2 * a)
    x2 = (-b - sqrt(discriminant)) / (2 * a)
    print("x1: ", x1, ",", "x2: ", x2)
elif sqrt(discriminant) == 0:
    x = (-b) / (2 * a)
    print("x: ", x)
else:
    print("Решения нет")
