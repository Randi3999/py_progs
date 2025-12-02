import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

class ThemeManager:
    @staticmethod
    def set_dark_theme(app):
        """Устанавливает тёмную тему"""
        app.setStyle("Fusion")

        dark_palette = QPalette()

        # Базовые цвета
        dark_colors = {
            QPalette.Window: (45, 45, 45),
            QPalette.WindowText: (255, 255, 255),
            QPalette.Base: (25, 25, 25),
            QPalette.AlternateBase: (53, 53, 53),
            QPalette.ToolTipBase: (255, 255, 255),
            QPalette.ToolTipText: (255, 255, 255),
            QPalette.Text: (255, 255, 255),
            QPalette.Button: (53, 53, 53),
            QPalette.ButtonText: (255, 255, 255),
            QPalette.BrightText: (255, 0, 0),
            QPalette.Link: (42, 130, 218),
            QPalette.Highlight: (42, 130, 218),
            QPalette.HighlightedText: (0, 0, 0)
        }

        for role, color in dark_colors.items():
            dark_palette.setColor(role, QColor(*color))

        app.setPalette(dark_palette)

        # Дополнительные стили CSS
        app.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
            }

            QPushButton {
                background-color: #3a3a3a;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }

            QPushButton:hover {
                background-color: #4a4a4a;
                border: 1px solid #666;
            }

            QPushButton:pressed {
                background-color: #2a2a2a;
            }

            QLineEdit, QTextEdit, QPlainTextEdit {
                background-color: #353535;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
                selection-background-color: #2a82da;
            }

            QComboBox {
                background-color: #353535;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
            }

            QComboBox::drop-down {
                border: none;
            }

            QComboBox QAbstractItemView {
                background-color: #353535;
                color: white;
                selection-background-color: #2a82da;
            }

            QCheckBox {
                spacing: 5px;
            }

            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }

            QTabWidget::pane {
                border: 1px solid #555;
                background-color: #2d2d2d;
            }

            QTabBar::tab {
                background-color: #3a3a3a;
                color: white;
                padding: 8px 16px;
                margin-right: 2px;
            }

            QTabBar::tab:selected {
                background-color: #505050;
            }

            QTabBar::tab:hover:!selected {
                background-color: #454545;
            }

            QScrollBar:vertical {
                border: none;
                background-color: #353535;
                width: 12px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background-color: #555;
                border-radius: 6px;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #666;
            }
        """)

    @staticmethod
    def set_light_theme(app):
        """Устанавливает светлую тему (по умолчанию)"""
        app.setStyle("Fusion")
        app.setPalette(app.style().standardPalette())
        app.setStyleSheet("")  # Сбрасываем стили

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_theme = True
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Переключатель тем")
        self.setGeometry(100, 100, 500, 400)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        main_layout = QVBoxLayout(central_widget)

        # Панель инструментов
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Кнопка переключения темы в тулбаре
        theme_action = QAction("🌙 Тёмная тема", self)
        theme_action.triggered.connect(self.toggle_theme)
        toolbar.addAction(theme_action)

        # Вкладки
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # Первая вкладка
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)

        # Разные виджеты для демонстрации
        self.create_demo_widgets(tab1_layout)
        tab_widget.addTab(tab1, "Основная")

        # Вторая вкладка
        tab2 = QWidget()
        tab2_layout = QVBoxLayout(tab2)

        text_edit = QTextEdit()
        text_edit.setPlaceholderText("Текстовое поле...")
        tab2_layout.addWidget(text_edit)

        tab_widget.addTab(tab2, "Текст")

        # Статусбар
        self.statusBar().showMessage("Тёмная тема активна")

    def create_demo_widgets(self, layout):
        """Создаёт демонстрационные виджеты"""
        # Группа настроек
        group = QGroupBox("Настройки")
        group_layout = QVBoxLayout()

        # Чекбоксы
        self.check1 = QCheckBox("Опция 1")
        self.check2 = QCheckBox("Опция 2")
        self.check3 = QCheckBox("Опция 3")

        group_layout.addWidget(self.check1)
        group_layout.addWidget(self.check2)
        group_layout.addWidget(self.check3)

        group.setLayout(group_layout)
        layout.addWidget(group)

        # Поля ввода
        form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.age_spin = QSpinBox()
        self.age_spin.setRange(0, 150)

        form_layout.addRow("Имя:", self.name_edit)
        form_layout.addRow("Email:", self.email_edit)
        form_layout.addRow("Возраст:", self.age_spin)

        layout.addLayout(form_layout)

        # Кнопки
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Отмена")
        self.apply_button = QPushButton("Применить")

        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.apply_button)

        layout.addLayout(button_layout)

        # Прогресс бар
        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        # Слайдер
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.progress.setValue)
        layout.addWidget(self.slider)

    def toggle_theme(self):
        """Переключает между тёмной и светлой темами"""
        if self.dark_theme:
            ThemeManager.set_light_theme(QApplication.instance())
            self.dark_theme = False
            self.statusBar().showMessage("Светлая тема активна")
        else:
            ThemeManager.set_dark_theme(QApplication.instance())
            self.dark_theme = True
            self.statusBar().showMessage("Тёмная тема активна")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Устанавливаем тёмную тему по умолчанию
    ThemeManager.set_dark_theme(app)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
