"""
В архиве voina-i-mir.zip лежит роман Льва Толстого «Война и мир». Напишите программу, которая подсчитает статистику по буквам (русского и латинского алфавита) в этом романе и выведет результат в текстовый файл. Результат должен быть отсортирован по частоте встречаемости букв (по возрастанию или   убыванию). Регистр символов имеет значение. Постарайтесь написать программу так, чтобы для её работы не требовалась распаковка  архива “вручную” (изучите самостоятельно модуль zipfile для распаковки архива). (4 балла)
Ответ должен быть в таком виде (доли от 1):
Й 0.00000126
Z 0.00000253
W 0.00000674
Щ 0.00000716
….
и 0.06492206
а 0.07803966
е 0.07942622
о 0.11040234
"""
import zipfile
import os
from collections import Counter

def count_letters_simple():
    """Упрощенная версия с запросом пути у пользователя"""
    
    # Запрашиваем путь к архиву
    while True:
        zip_path = "../voina-i-mir.zip"
        if os.path.exists(zip_path):
            break
        print("Файл не найден. Попробуйте снова.")
    
    # Определяем допустимые символы
    russian_letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    latin_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    valid_chars = set(russian_letters + latin_letters)
    
    # Счетчик
    counter = Counter()
    total = 0
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # Обрабатываем все файлы в архиве
            for filename in zf.namelist():
                if not filename.endswith('/'):  # Пропускаем папки
                    with zf.open(filename) as f:
                        text = f.read().decode('utf-8')
                        for char in text:
                            if char in valid_chars:
                                counter[char] += 1
                                total += 1
    except Exception as e:
        print(f"Ошибка: {e}")
        return
    
    # Записываем результат
    with open('letter_statistics.txt', 'w', encoding='utf-8') as f:
        for char, count in sorted(counter.items(), key=lambda x: x[1], reverse=True):
            frequency = count / total
            f.write(f"{char} {frequency:.8f}\n")
    
    print(f"Готово! Обработано {total} букв.")
    print("Результат сохранен в файл 'letter_statistics.txt'")

# Запускаем программу
count_letters_simple()
