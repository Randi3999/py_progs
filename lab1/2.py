a = int(input("Напишите коэфициент a: "))
b = int(input("Напишите коэфициент b: "))
c = int(input("Напишите коэфициент c: "))

if a != 0 and b != 0 and c != 0:
    discriminant = (b ** 2) - (4 * a * c)
elif a == 0:
    
    

if discriminant > 0:
    x1 = (-b + discriminant) / (2 * a)
    x2 = (-b - discriminant) / (2 * a)
    print("x1: ", x1, ",", "x2: ", x2)
elif discriminant == 0:
    x = (-b) / (2 * a)
    print("x: ", x)
else:
    print("Решения нет")
