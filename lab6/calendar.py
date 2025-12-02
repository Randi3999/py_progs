from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFormLayout, QLineEdit
from PyQt5.QtCore import Qt
import sys

class DateTimeApp(QWidget):
    def __init__(self):
        super().__init__()
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

        # Настройка календаря (опционально)
        self.date_time_edit.calendarWidget().setGridVisible(True)

        layout.addWidget(self.date_time_edit)

        # Кнопка для получения выбранного значения
        btn = QPushButton("Получить выбранную дату")
        btn.clicked.connect(self.get_selected_datetime)
        layout.addWidget(btn)

        # Метка для отображения результата
        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.setWindowTitle("Выбор даты и времени")
        self.setGeometry(300, 300, 300, 200)

    def get_selected_datetime(self):
        selected_datetime = self.date_time_edit.dateTime()
        self.result_label.setText(f"Выбрано: {selected_datetime.toString('dd.MM.yyyy HH:mm')}")

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def open_add_event(self, layout):
        self.new_window = QWidget()
        self.new_window.setWindowTitle("Добавление события...")
        self.new_window.setFixedSize(500,650)
        self.new_window.move(50,50)
        # Создаем layout для нового окна
        main_layout = QVBoxLayout()

        # Создаем форму
        form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        form_layout.addRow("Название:", self.name_edit)

        # Добавляем форму в основной layout
        main_layout.addLayout(form_layout)

        # Добавляем растяжку внизу
        main_layout.addStretch()

        # Устанавливаем layout для нового окна
        self.new_window.setLayout(main_layout)
        self.new_window.show()

    def open_view_events(self):
        self.new_window = QWidget()
        self.new_window.setWindowTitle("Просмотр событий")
        self.new_window.setFixedSize(500,650)
        self.new_window.move(50,50)
        self.new_window.show()

    def initUI(self):
        self.setWindowTitle("Я календарь переверну...")
        self.setFixedSize(500,650)

        layout = QVBoxLayout()

        # Добавляем растяжку сверху
        layout.addStretch()

        # Создаем и настраиваем кнопку
        button_add_event = QPushButton("Добавить Событие")
        button_add_event.setFixedSize(120, 40)
        button_add_event.clicked.connect(self.open_add_event)  # Связываем кнопку с методом

        button_view_events = QPushButton("Просмотр событий")
        button_view_events.setFixedSize(120,40)
        button_view_events.clicked.connect(self.open_view_events)
        # Центрируем кнопку в layout
        layout.addWidget(button_add_event, 0, Qt.AlignCenter)
        layout.addWidget(button_view_events, 0, Qt.AlignCenter)

        # Добавляем растяжку снизу
        layout.addStretch()

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
