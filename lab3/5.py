"""
Есть два текстовых файла. В одном записаны слова на русском языке, на другом – в тех же строках их перевод на английский язык. Написать тестирующую программу, которая последовательно выводит слова из первого файла и ждет, когда пользователь введет перевод слова на английский язык. После этого программа должна сравнить правильность перевода и вывести сообщение «Верно» или «Неверно». После окончания работы программы поставить оценку.
"""
def test_translation(russian_file, english_file):
    """
    Тестирующая программа для проверки перевода слов
    """

    # Читаем файлы
    try:
        with open(russian_file, 'r', encoding='utf-8') as ru_file:
            russian_words = [line.strip() for line in ru_file if line.strip()]

        with open(english_file, 'r', encoding='utf-8') as en_file:
            english_words = [line.strip() for line in en_file if line.strip()]
    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден - {e}")
        return
    except Exception as e:
        print(f"Ошибка при чтении файлов: {e}")
        return

    # Проверяем, что количество слов совпадает
    if len(russian_words) != len(english_words):
        print("Ошибка: количество строк в файлах не совпадает!")
        return

    correct_answers = 0
    total_words = len(russian_words)

    print("=" * 50)
    print("ТЕСТИРОВАНИЕ ПЕРЕВОДА")
    print("=" * 50)

    # Проходим по всем словам
    for i, (ru_word, correct_en) in enumerate(zip(russian_words, english_words), 1):
        print(f"\nСлово {i}/{total_words}: {ru_word}")

        # Получаем ответ пользователя
        user_answer = input("Введите перевод на английский: ").strip().lower()

        # Сравниваем с правильным ответом (игнорируем регистр и лишние пробелы)
        if user_answer == correct_en.lower():
            print("✅ Верно!")
            correct_answers += 1
        else:
            print(f"❌ Неверно! Правильный ответ: {correct_en}")

    # Выводим результаты
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 50)

    score = correct_answers / total_words * 100
    print(f"Правильных ответов: {correct_answers} из {total_words}")
    print(f"Процент правильных ответов: {score:.1f}%")

    # Ставим оценку
    if score >= 90:
        grade = "5 (Отлично)"
    elif score >= 75:
        grade = "4 (Хорошо)"
    elif score >= 60:
        grade = "3 (Удовлетворительно)"
    else:
        grade = "2 (Неудовлетворительно)"

    print(f"Оценка: {grade}")

# Основная программа
if __name__ == "__main__":
    # Имена файлов (можно изменить на свои)
    russian_file = "russian_words.txt"
    english_file = "english_words.txt"

    print("Программа для тестирования перевода слов")
    print("Файлы должны быть в формате: одно слово на строку")
    print(f"Русские слова: {russian_file}")
    print(f"Английские слова: {english_file}")
    print()

    test_translation(russian_file, english_file)
