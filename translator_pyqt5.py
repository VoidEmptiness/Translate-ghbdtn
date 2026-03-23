import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QFrame, QStatusBar
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont

class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Простой переводчик [fq-хай")
        self.setGeometry(100, 100, 600, 500)
        self.translation_map = {}
        self.load_base_file()
        self.create_widgets()
        
    def load_base_file(self):
        try:
            base_file = "base.txt"
            if not os.path.exists(base_file):
                self.show_message("Ошибка", f"Файл {base_file} не найден!")
                return
            with open(base_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '-' in line:
                        parts = line.split('-', 1)
                        if len(parts) == 2:
                            from_char, to_char = parts
                            self.translation_map[from_char] = to_char
            if not self.translation_map:
                self.show_message("Предупреждение", "Файл base.txt пуст или содержит некорректные данные")
        except Exception as e:
            self.show_message("Ошибка", f"Не удалось загрузить файл base.txt: {e}")
            
    def create_widgets(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        input_label = QLabel("Текст для перевода:")
        layout.addWidget(input_label)
        
        self.input_text = QTextEdit()
        self.input_text.setFont(QFont("Arial", 11))
        self.input_text.setFixedHeight(120)
        layout.addWidget(self.input_text)
        
        button_layout = QHBoxLayout()
        
        self.copy_btn = QPushButton("Копировать")
        self.copy_btn.clicked.connect(self.copy_text)
        button_layout.addWidget(self.copy_btn)
        
        self.paste_btn = QPushButton("Вставить")
        self.paste_btn.clicked.connect(self.paste_text)
        button_layout.addWidget(self.paste_btn)
        
        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.clicked.connect(self.clear_text)
        button_layout.addWidget(self.clear_btn)
        
        self.swap_btn = QPushButton("Поменять местами")
        self.swap_btn.clicked.connect(self.swap_text)
        button_layout.addWidget(self.swap_btn)
        
        layout.addLayout(button_layout)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        output_label = QLabel("Результат перевода:")
        layout.addWidget(output_label)
        
        self.output_text = QTextEdit()
        self.output_text.setFont(QFont("Arial", 11))
        self.output_text.setFixedHeight(120)
        layout.addWidget(self.output_text)
        
        self.status_bar = QStatusBar()
        self.status_bar.showMessage(f"Загружено {len(self.translation_map)} символов для перевода")
        self.setStatusBar(self.status_bar)
        
        self.input_text.textChanged.connect(self.on_text_change)
        
        self.copy_btn.setShortcut("Ctrl+C")
        self.paste_btn.setShortcut("Ctrl+V")
        self.clear_btn.setShortcut("Ctrl+L")
        self.swap_btn.setShortcut("Ctrl+S")
        
    def translate_text(self):
        input_text = self.input_text.toPlainText().strip()
        if not input_text:
            self.output_text.clear()
            return
        translated = self.translate_string(input_text)
        self.output_text.setPlainText(translated)
        
    def on_text_change(self):
        if hasattr(self, '_timer'):
            self._timer.stop()
        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.translate_text)
        self._timer.start(100)
        
    def translate_string(self, text):
        result = []
        for char in text:
            if char in self.translation_map:
                result.append(self.translation_map[char])
            elif char.lower() in self.translation_map:
                translated_char = self.translation_map[char.lower()]
                result.append(translated_char.upper() if char.isupper() else translated_char)
            else:
                result.append(char)
        return ''.join(result)
        
    def clear_text(self):
        self.input_text.clear()
        self.output_text.clear()
        
    def copy_text(self):
        output_text = self.output_text.toPlainText().strip()
        if output_text:
            clipboard = QApplication.clipboard()
            clipboard.setText(output_text)
            
    def paste_text(self):
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()
        if clipboard_text:
            self.input_text.insertPlainText(clipboard_text)
            self.on_text_change()
            
    def swap_text(self):
        input_content = self.input_text.toPlainText().strip()
        output_content = self.output_text.toPlainText().strip()
        self.input_text.setPlainText(output_content)
        self.output_text.setPlainText(input_content)
        
    def show_message(self, title, message):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.warning(self, title, message)

def main():
    app = QApplication(sys.argv)
    translator = TranslatorApp()
    translator.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()