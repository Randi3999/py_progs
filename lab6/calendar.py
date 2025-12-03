import sys
import os
import psycopg2
from datetime import datetime, date
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import pygame

# ============================================================================
# КОНФИГУРАЦИЯ БАЗЫ ДАННЫХ
# ============================================================================
class Config:
    DB_CONFIG = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': '5432'
    }

    @staticmethod
    def get_connection():
        """Создание подключения к базе данных"""
        return psycopg2.connect(**Config.DB_CONFIG)

    @staticmethod
    def init_database():
        """Инициализация базы данных и создание таблицы, если она не существует"""
        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id SERIAL PRIMARY KEY,
                    event_date DATE NOT NULL,
                    event_name VARCHAR(255) NOT NULL
                )
            ''')

            conn.commit()
            cursor.close()
            conn.close()
            print("База данных инициализирована успешно")
        except Exception as e:
            print(f"Ошибка инициализации базы данных: {e}")
    LOGO_PATH = "календарь_лого_Климов.png"

# ============================================================================
# ОСНОВНОЕ ОКНО ПРИЛОЖЕНИЯ
# ============================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Календарь событий')
        self.setFixedSize(500, 400)
        self.background_enabled = False
        self.original_stylesheet = ""
        self.init_ui()
        self.init_tray_icon()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.central_widget = central_widget

        self.original_stylesheet = central_widget.styleSheet()

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        title_label = QLabel('Календарь событий')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('''
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin: 20px;
        ''')
        layout.addWidget(title_label)

        logo_label = QLabel()
        try:
            logo_pixmap = QPixmap(Config.LOGO_PATH)
            if logo_pixmap.isNull():
                logo_pixmap = QPixmap(400, 150)
                logo_pixmap.fill(QColor(52, 152, 219))
                painter = QPainter(logo_pixmap)
                painter.setBrush(QColor(241, 196, 15))
                painter.drawEllipse(150, 25, 100, 100)
                painter.setPen(QColor(44, 62, 80))
                painter.setFont(QFont('Arial', 24))
                painter.drawText(170, 90, "C")
                painter.end()
            else:
                logo_pixmap = logo_pixmap.scaled(400, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            logo_label.setPixmap(logo_pixmap)
        except Exception as e:
            print(f"Ошибка загрузки логотипа: {e}")
            logo_pixmap = QPixmap(400, 150)
            logo_pixmap.fill(QColor(52, 152, 219))
            logo_label.setPixmap(logo_pixmap)

        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton('Добавить событие')
        self.add_button.setStyleSheet('''
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 15px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        ''')
        self.add_button.clicked.connect(self.open_add_event_window)
        buttons_layout.addWidget(self.add_button)

        self.view_button = QPushButton('Просмотр событий')
        self.view_button.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 15px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        self.view_button.clicked.connect(self.open_view_events_window)
        buttons_layout.addWidget(self.view_button)

        layout.addLayout(buttons_layout)

        self.music_button = QPushButton('Музыкальное сопровождение')
        self.music_button.setCheckable(True)
        self.music_button.setChecked(False)
        self.music_button.setStyleSheet('''
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:checked {
                background-color: #2ecc71;
            }
        ''')
        self.music_button.clicked.connect(self.toggle_music)
        layout.addWidget(self.music_button)

    def open_add_event_window(self):
        """Открыть окно добавления события"""
        self.add_window = AddEventWindow()
        self.add_window.show()

    def open_view_events_window(self):
        """Открыть окно просмотра событий"""
        self.view_window = ViewEventsWindow()
        self.view_window.show()

    def toggle_music(self):
        """Включение/выключение музыкального сопровождения и фона"""
        if self.music_button.isChecked():
            try:
                self.play_music()
                self.music_button.setText('Музыкальное сопровождение (вкл)')
                print("Музыка включена")

                self.enable_background()
                print("Фоновое изображение включено")

            except Exception as e:
                print(f"Ошибка воспроизведения музыки: {e}")
                self.music_button.setChecked(False)
        else:
            self.stop_music()
            self.music_button.setText('Музыкальное сопровождение')
            print("Музыка выключена")

            self.disable_background()
            print("Фоновое изображение выключено")

    def enable_background(self):
        try:
            background_path = "background_photo.jpg"

            if not os.path.exists(background_path):
                print(f"Файл фонового изображения не найден: {background_path}")
                print(f"Текущая директория: {os.getcwd()}")
                print("Создайте файл background_photo.jpg в той же директории")
                return

            abs_background_path = os.path.abspath(background_path)
            if os.name == 'nt':
                abs_background_path = abs_background_path.replace('\\', '/')

            background_style = f"""
                #central_widget {{
                    background-image: url('file://{abs_background_path}');
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                    background-size: cover;
                    border-radius: 10px;
                }}

                QLabel {{
                    background-color: rgba(255, 255, 255, 0.8);
                    border-radius: 5px;
                    padding: 5px;
                    font-weight: bold;
                }}

                QPushButton {{
                    background-color: rgba(39, 174, 96, 0.9);
                    color: white;
                    border: 2px solid rgba(255, 255, 255, 0.5);
                    padding: 15px;
                    font-size: 16px;
                    border-radius: 5px;
                    font-weight: bold;
                }}

                QPushButton:hover {{
                    background-color: rgba(34, 153, 84, 0.9);
                    border: 2px solid rgba(255, 255, 255, 0.8);
                }}

                QPushButton#view_button {{
                    background-color: rgba(52, 152, 219, 0.9);
                }}

                QPushButton#view_button:hover {{
                    background-color: rgba(41, 128, 185, 0.9);
                }}

                QPushButton#music_button:checked {{
                    background-color: rgba(46, 204, 113, 0.9);
                }}
            """

            self.central_widget.setObjectName("central_widget")

            self.view_button.setObjectName("view_button")
            self.music_button.setObjectName("music_button")

            self.central_widget.setStyleSheet(background_style)
            self.background_enabled = True

            print(f"Фоновое изображение установлено: {abs_background_path}")

        except Exception as e:
            print(f"Ошибка при установке фонового изображения: {e}")
            import traceback
            traceback.print_exc()

    def disable_background(self):
        try:
            self.central_widget.setObjectName("")
            self.view_button.setObjectName("")
            self.music_button.setObjectName("")

            self.central_widget.setStyleSheet(self.original_stylesheet)
            self.background_enabled = False

            self.add_button.setStyleSheet('''
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    padding: 15px;
                    font-size: 16px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #229954;
                }
            ''')

            self.view_button.setStyleSheet('''
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 15px;
                    font-size: 16px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            ''')

            self.music_button.setStyleSheet('''
                QPushButton {
                    background-color: #9b59b6;
                    color: white;
                    border: none;
                    padding: 10px;
                    font-size: 14px;
                    border-radius: 5px;
                    margin-top: 20px;
                }
                QPushButton:hover {
                    background-color: #8e44ad;
                }
                QPushButton:checked {
                    background-color: #2ecc71;
                }
            ''')

            print("Фоновое изображение отключено")

        except Exception as e:
            print(f"Ошибка при отключении фонового изображения: {e}")

    def play_music(self):
        try:
            if not hasattr(self, 'pygame_initialized'):
                pygame.mixer.init()
                self.pygame_initialized = True

            pygame.mixer.music.load("music.mp3")
            pygame.mixer.music.play(-1)
        except ImportError:
            print("Ошибка: не установлен модуль pygame. Установите его: pip install pygame")

            if not hasattr(self, 'media_player'):
                self.media_player = QMediaPlayer()
                self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile("music.mp3")))

            self.media_player.play()

    def stop_music(self):
        try:
            if hasattr(self, 'pygame_initialized'):
                pygame.mixer.music.stop()
        except:
            if hasattr(self, 'media_player'):
                self.media_player.stop()

    def init_tray_icon(self):
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)

            try:
                tray_pixmap = QPixmap(Config.LOGO_PATH)
                if not tray_pixmap.isNull():
                    icon_size = QSize(32, 32)
                    tray_pixmap = tray_pixmap.scaled(icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.tray_icon.setIcon(QIcon(tray_pixmap))
                    print(f"Иконка трея загружена из: {Config.LOGO_PATH}")
                else:
                    print("Логотип не найден или поврежден, создаем иконку по умолчанию")
                    self.create_default_tray_icon()
            except Exception as e:
                print(f"Ошибка загрузки иконки для трея: {e}")
                self.create_default_tray_icon()

            tray_menu = QMenu()

            show_action = QAction("Показать", self)
            show_action.triggered.connect(self.show_window)
            tray_menu.addAction(show_action)

            hide_action = QAction("Скрыть", self)
            hide_action.triggered.connect(self.hide_window)
            tray_menu.addAction(hide_action)

            tray_menu.addSeparator()

            exit_action = QAction("Выход", self)
            exit_action.triggered.connect(self.close_application)
            tray_menu.addAction(exit_action)

            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.activated.connect(self.tray_icon_activated)

            self.tray_icon.show()

            self.tray_icon.setToolTip("Календарь событий")

    def create_default_tray_icon(self):
        size = 128
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QColor(52, 152, 219))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(2, 2, size-4, size-4)

        painter.setBrush(QColor(241, 196, 15))
        painter.drawEllipse(size//4, size//4, size//2, size//2)

        painter.setPen(QColor(44, 62, 80))
        painter.setFont(QFont('Arial', size//3))
        painter.drawText(size//3, size*2//3, "К")
        painter.end()

        self.tray_icon.setIcon(QIcon(pixmap))

    def show_window(self):
        self.show()
        self.activateWindow()
        self.raise_()

    def hide_window(self):
        self.hide()

    def close_application(self):
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        QApplication.quit()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show_window()

    def closeEvent(self, event):
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Календарь событий",
                "Приложение свернуто в трей",
                QSystemTrayIcon.Information,
                2000
            )
        else:
            event.accept()

# ============================================================================
# ОКНО ДОБАВЛЕНИЯ СОБЫТИЯ
# ============================================================================
class AddEventWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить событие')
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel('Добавление нового события')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('''
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            margin: 10px;
        ''')
        layout.addWidget(title_label)

        name_layout = QHBoxLayout()
        name_label = QLabel('Название события:')
        name_label.setFixedWidth(150)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Введите название события')
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        date_layout = QHBoxLayout()
        date_label = QLabel('Дата события:')
        date_label.setFixedWidth(150)
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat('dd.MM.yyyy')
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input)
        layout.addLayout(date_layout)

        buttons_layout = QHBoxLayout()

        add_button = QPushButton('Добавить')
        add_button.setStyleSheet('''
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        ''')
        add_button.clicked.connect(self.add_event)
        buttons_layout.addWidget(add_button)

        cancel_button = QPushButton('Отмена')
        cancel_button.setStyleSheet('''
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        ''')
        cancel_button.clicked.connect(self.close)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

    def add_event(self):
        """Добавить событие в базу данных"""
        event_name = self.name_input.text().strip()
        event_date = self.date_input.date().toString('yyyy-MM-dd')

        if not event_name:
            self.status_label.setText('Введите название события!')
            self.status_label.setStyleSheet('color: #e74c3c;')
            return

        try:
            conn = Config.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO events (event_date, event_name) VALUES (%s, %s)",
                (event_date, event_name)
            )

            conn.commit()
            cursor.close()
            conn.close()

            self.status_label.setText('Событие успешно добавлено!')
            self.status_label.setStyleSheet('color: #27ae60;')

            self.name_input.clear()
            self.date_input.setDate(QDate.currentDate())

        except Exception as e:
            self.status_label.setText(f'Ошибка: {str(e)}')
            self.status_label.setStyleSheet('color: #e74c3c;')

# ============================================================================
# ОКНО ПРОСМОТРА СОБЫТИЙ
# ============================================================================
class ViewEventsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Просмотр событий')
        self.setFixedSize(800, 600)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # --------------------------------------------------------------------
        # Фрейм A: Текущая дата и день недели (вверху)
        # --------------------------------------------------------------------
        frame_a = QFrame()
        frame_a.setFrameStyle(QFrame.Box | QFrame.Raised)
        frame_a.setStyleSheet('background-color: #ecf0f1; padding: 10px;')
        frame_a_layout = QHBoxLayout()

        current_date = datetime.now()
        date_label = QLabel(f'Текущая дата: {current_date.strftime("%d.%m.%Y")}')
        date_label.setStyleSheet('font-size: 16px; font-weight: bold;')

        weekday_label = QLabel(f'День недели: {self.get_russian_weekday(current_date)}')
        weekday_label.setStyleSheet('font-size: 16px; font-weight: bold;')

        frame_a_layout.addWidget(date_label)
        frame_a_layout.addStretch()
        frame_a_layout.addWidget(weekday_label)
        frame_a.setLayout(frame_a_layout)
        main_layout.addWidget(frame_a)

        # --------------------------------------------------------------------
        # Основной контейнер (левая и правая части)
        # --------------------------------------------------------------------
        container = QHBoxLayout()

        # --------------------------------------------------------------------
        # Фрейм B: Ввод года и выбор месяца (левая часть)
        # --------------------------------------------------------------------
        frame_b = QFrame()
        frame_b.setFrameStyle(QFrame.Box | QFrame.Raised)
        frame_b.setFixedWidth(250)
        frame_b.setStyleSheet('background-color: #f8f9fa; padding: 15px;')
        frame_b_layout = QVBoxLayout()

        year_label = QLabel('Год:')
        year_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        self.year_input = QSpinBox()
        self.year_input.setRange(2000, 2100)
        self.year_input.setValue(current_date.year)

        month_label = QLabel('Месяц:')
        month_label.setStyleSheet('font-size: 14px; font-weight: bold; margin-top: 10px;')
        self.month_combo = QComboBox()
        months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        self.month_combo.addItems(months)
        self.month_combo.setCurrentIndex(current_date.month - 1)

        frame_b_layout.addWidget(year_label)
        frame_b_layout.addWidget(self.year_input)
        frame_b_layout.addWidget(month_label)
        frame_b_layout.addWidget(self.month_combo)
        frame_b_layout.addStretch()
        frame_b.setLayout(frame_b_layout)

        # --------------------------------------------------------------------
        # Фрейм C: Вывод информации о событиях (правая часть)
        # --------------------------------------------------------------------
        frame_c = QFrame()
        frame_c.setFrameStyle(QFrame.Box | QFrame.Raised)
        frame_c.setStyleSheet('background-color: white;')
        frame_c_layout = QVBoxLayout()

        table_header = QLabel('События')
        table_header.setAlignment(Qt.AlignCenter)
        table_header.setStyleSheet('''
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
            border-bottom: 2px solid #3498db;
        ''')
        frame_c_layout.addWidget(table_header)

        self.events_table = QTableWidget()
        self.events_table.setColumnCount(5)
        self.events_table.setHorizontalHeaderLabels([
            'Название события',
            'Дата события',
            'День недели',
            'Дней до/после',
            'Статус'
        ])
        self.events_table.horizontalHeader().setStretchLastSection(True)
        self.events_table.setEditTriggers(QTableWidget.NoEditTriggers)

        frame_c_layout.addWidget(self.events_table)
        frame_c.setLayout(frame_c_layout)

        container.addWidget(frame_b)
        container.addWidget(frame_c)
        main_layout.addLayout(container)

        # --------------------------------------------------------------------
        # Фрейм D: Кнопки "Просмотр" и "Назад" (внизу)
        # --------------------------------------------------------------------
        frame_d = QFrame()
        frame_d.setFrameStyle(QFrame.Box | QFrame.Raised)
        frame_d.setStyleSheet('background-color: #ecf0f1; padding: 10px;')
        frame_d_layout = QHBoxLayout()

        view_button = QPushButton('Просмотр')
        view_button.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 14px;
                border-radius: 5px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        view_button.clicked.connect(self.load_events)

        back_button = QPushButton('Назад')
        back_button.setStyleSheet('''
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 14px;
                border-radius: 5px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        ''')
        back_button.clicked.connect(self.close)

        frame_d_layout.addStretch()
        frame_d_layout.addWidget(view_button)
        frame_d_layout.addWidget(back_button)
        frame_d_layout.addStretch()
        frame_d.setLayout(frame_d_layout)
        main_layout.addWidget(frame_d)

        QTimer.singleShot(100, self.load_events)

    def get_russian_weekday(self, date_obj):
        """Получить русское название дня недели"""
        weekdays = {
            0: 'Понедельник',
            1: 'Вторник',
            2: 'Среда',
            3: 'Четверг',
            4: 'Пятница',
            5: 'Суббота',
            6: 'Воскресенье'
        }
        return weekdays[date_obj.weekday()]

    def calculate_days_difference(self, event_date):
        """Рассчитать разницу в днях между текущей датой и датой события"""
        today = date.today()
        diff = (event_date - today).days

        if diff > 0:
            return f'Через {diff} дн.'
        elif diff < 0:
            return f'{abs(diff)} дн. назад'
        else:
            return '0 дн.'

    def load_events(self):
        """Загрузить события из базы данных"""
        try:
            year = self.year_input.value()
            month = self.month_combo.currentIndex() + 1

            conn = Config.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT event_name, event_date
                FROM events
                WHERE EXTRACT(YEAR FROM event_date) = %s
                AND EXTRACT(MONTH FROM event_date) = %s
                ORDER BY event_date
            ''', (year, month))

            events = cursor.fetchall()
            cursor.close()
            conn.close()

            self.events_table.setRowCount(len(events))

            today = date.today()

            for row, (event_name, event_date) in enumerate(events):
                name_item = QTableWidgetItem(event_name)

                date_item = QTableWidgetItem(event_date.strftime('%d.%m.%Y'))

                weekday_item = QTableWidgetItem(self.get_russian_weekday(event_date))

                days_diff = self.calculate_days_difference(event_date)
                days_item = QTableWidgetItem(days_diff)

                status = ''
                if event_date == today:
                    status = 'Сегодня'
                    for col in range(5):
                        item = self.events_table.item(row, col)
                        if item:
                            item.setBackground(QColor(255, 255, 200))

                status_item = QTableWidgetItem(status)

                self.events_table.setItem(row, 0, name_item)
                self.events_table.setItem(row, 1, date_item)
                self.events_table.setItem(row, 2, weekday_item)
                self.events_table.setItem(row, 3, days_item)
                self.events_table.setItem(row, 4, status_item)

            self.events_table.resizeColumnsToContents()

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить события: {str(e)}')

# ============================================================================
# ЗАПУСК ПРИЛОЖЕНИЯ
# ============================================================================
def main():
    Config.init_database()

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
