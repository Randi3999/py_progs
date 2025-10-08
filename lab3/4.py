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
from collections import Counter


def analyze_war_and_peace_simple():
    archive_path = "voyna-i-mir.zip"

    try:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            text_file_name = None
            for file_info in zip_ref.filelist:
                if file_info.filename.endswith('.txt'):
                    text_file_name = file_info.filename
                    break

            if not text_file_name:
                raise FileNotFoundError("Текстовый файл не найден в архиве")

            with zip_ref.open(text_file_name, 'r') as file:
                text = file.read().decode('utf-8')

            letters_counter = Counter()
            for char in text:
                if char.isalpha() and (('\u0400' <= char <= '\u04FF') or
                                       ('a' <= char <= 'z') or
                                       ('A' <= char <= 'Z')):
                    letters_counter[char] += 1

            total_letters = sum(letters_counter.values())

            with open('letter_statistics.txt', 'w', encoding='utf-8') as output_file:
                for letter, count in sorted(letters_counter.items(),
                                            key=lambda x: x[1], reverse=True):
                    frequency = count / total_letters
                    output_file.write(f"{letter} {frequency:.8f}\n")

            print("Анализ завершен! Результат в 'letter_statistics.txt'")

    except Exception as e:
        print(f"Ошибка: {e}")


analyze_war_and_peace_simple()
