# приложение календарь

import sys
import psycopg2

# проверка базы данных
try:
    connection = psycopg2.connect(user = "postgres",
            password = "postgres",
            host = "localhost",
            port = "5432",
            database = "postgres"
            )

except:
    print("Подключение к БД отсутствует. Включите БД!")
    sys.exit()

print("Подключение к БД успешно установлено!")

cursor = connection.cursor()

# создание таблицы (если не создана)
cursor.execute("""
               CREATE TABLE IF NOT EXISTS calendar (
                    id SERIAL PRIMARY KEY,
                    date TIMESTAMPTZ,
                    name TEXT
               )
               """)
def create_event():
    print("\nСоздание события...")
    name = input("Введите название события: ")
    date = input("Введите дату события(формат: YYYY/MM/dd hh/mm/ss): ")
    try:
        cursor.execute("INSERT INTO calendar (name, date) VALUES (%s, %s)", (name, date))
        connection.commit()
        print("Событие создано.")
    except Exception as e:
        connection.rollback()
        print(f"Ошибка при создании события: {e}")

def del_event():
    print("\nУдаление события.")
    ID = int(input("Введите id события: "))
    try:
        cursor.execute("DELETE FROM calendar WHERE id = %s", (ID,))
        connection.commit()
        if cursor.rowcount > 0:
            print("Событие удалено.")
        else:
            print("Событие с таким id не найдено.")
    except ValueError:
        print("Ошибка: id должен быть числом.")
    except Exception as e:
        connection.rollback()
        print(f"Ошибка при удалении события: {e}")

def view_events():
    print("\nПросмотр всех событий:")
    cursor.execute("""
                   SELECT * FROM calendar;
                   """)
    events = cursor.fetchall()

    if not events:
        print("Событий не найдено.")
        return

    print("="*60)
    print(f"{'ID':<5} {'Дата':<25} {'Событие':<30}")
    print("="*60)

    for event in events:
        event_id = event[0]
        event_date = event[1].strftime("%Y-%m-%d %H:%M:%S") if event[1] else ""
        event_name = event[2]

        print(f"{event_id:<5} {event_date:<25} {event_name:<30}")
    print("="*60)
    print(f"Всего событий: {len(events)}")



def menu():
    print("""
Меню:
1) Создание события
2) Удаление события
3) Просмотр событий
0) Выход"
    """)

def main():
    print("Я календарь переверну...")
    while True:
        menu()
        try:
            choice = int(input("Выберете пункт меню: "))
            if choice == 1:
                create_event()
            elif choice == 2:
                del_event()
            elif choice == 3:
                view_events()
            elif choice == 0:
                print("Выход из программы...")
                break
            else:
                print("Введите верный пункт меню!")
        except ValueError:
            print("Ошибка: введите число")
        except KeyboardInterrupt:
            print("\nПрограмма прервана пользователем")
            break

main()
