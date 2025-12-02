import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime, Qt

class DateTimeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_datetime = None  # Переменная для хранения выбранной даты и времени
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Метка
        label = QLabel("Выберите дату и время:")
        layout.addWidget(label)

        # Поле для выбора даты и времени
        self.date_time_edit = QDateTimeEdit(self)
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())
        self.date_time_edit.setCalendarPopup(True)  # Включаем всплывающий календарь
        self.date_time_edit.setDisplayFormat("dd.MM.yyyy HH:mm")

        # Связываем сигнал изменения даты с обработчиком
        self.date_time_edit.dateTimeChanged.connect(self.update_datetime_variable)

        layout.addWidget(self.date_time_edit)

        # Кнопка для вывода в консоль
        btn_print = QPushButton("Вывести в консоль")
        btn_print.clicked.connect(self.print_to_console)
        layout.addWidget(btn_print)

        # Кнопка для принудительного обновления переменной
        btn_update = QPushButton("Обновить переменную")
        btn_update.clicked.connect(self.force_update_variable)
        layout.addWidget(btn_update)

        # Метка для отображения текущего значения
        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        # Инициализируем переменную при запуске
        self.update_datetime_variable()

        self.setLayout(layout)
        self.setWindowTitle("Выбор даты и времени")
        self.setGeometry(300, 300, 300, 250)

    def update_datetime_variable(self):
        """Обновляет переменную selected_datetime при изменении значения в виджете"""
        selected_datetime = self.date_time_edit.dateTime()
        self.selected_datetime = selected_datetime

        # Форматируем в нужный формат
        formatted_datetime = selected_datetime.toString("yyyy/MM/dd hh:mm:ss")

        # Обновляем метку
        self.result_label.setText(f"Текущее значение: {formatted_datetime}")

        return formatted_datetime

    def force_update_variable(self):
        """Принудительно обновляет переменную (на всякий случай)"""
        formatted = self.update_datetime_variable()
        print(f"Переменная обновлена: {formatted}")

    def print_to_console(self):
        """Выводит значение переменной в консоль"""
        if self.selected_datetime:
            # Форматируем дату в нужный формат
            formatted = self.selected_datetime.toString("yyyy/MM/dd hh:mm:ss")

            print("-" * 50)
            print(f"Выбранная дата и время: {formatted}")
            print(f"Тип переменной: {type(self.selected_datetime)}")
            print(f"Сырые данные: {self.selected_datetime}")
            print("-" * 50)

            # Также можно сохранить в строковой переменной для дальнейшего использования
            datetime_str = formatted
            print(f"Строковое представление: {datetime_str}")

            # Обновляем метку
            self.result_label.setText(f"Выведено в консоль: {formatted}")
        else:
            print("Дата не выбрана!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DateTimeApp()
    ex.show()
    sys.exit(app.exec_())
