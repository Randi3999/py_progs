from random import choice
print("Привет! Это игра Камень, ножницы, бумага!")
cho = ['Камень','Ножницы','Бумага']
Value = str(input("Введите ваш ход: "))
n = 0
while(n == 0):
    KompValue = choice(cho)
    if Value == "Камень" and KompValue == "Ножницы":
        print("Ответ компьютера:", KompValue)
        print("Вы выйграли!")
        break
    elif Value == "Камень" and KompValue == "Бумага":
        print("Ответ компьютера:", KompValue)
        print("Вы проиграли!")
        break
    elif Value == "Камень" and KompValue == "Камень":
        print("Ответ компьютера:", KompValue)
        print("Ничья!")
        break
    elif Value == "Ножницы" and KompValue == "Камень":
        print("Ответ компьютера:", KompValue)
        print("Вы проиграли!")
        break
    elif Value == "Ножницы" and KompValue == "Ножницы":
        print("Ответ компьютера:", KompValue)
        print("Ничья!")
        break
    elif Value == "Ножницы" and KompValue == "Бумага":
        print("Ответ компьютера:", KompValue)
        print("Вы выйграли!")
        break
    elif Value == "Бумага" and KompValue == "Камень":
        print("Ответ компьютера:", KompValue)
        print("Вы выйграли!")
        break
    elif Value == "Бумага" and KompValue == "Ножницы":
        print("Ответ компьютера:", KompValue)
        print("Вы проиграли!")
        break
    elif Value == "Бумага" and KompValue == "Бумага":
        print("Ответ компьютера:", KompValue)
        print("Ничья!")
        break
