import sys, os, re, glob
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Переименование файлов")
        self.resize(800, 600)
        self.layout = QVBoxLayout(self)

        # Кнопка выбрать папку
        self.btn_choose = QPushButton("Указать папку")
        self.btn_choose.clicked.connect(self.choose_folder)
        self.layout.addWidget(self.btn_choose)

        # Таблица
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Имя файла", "Заголовок (## ...)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.SelectedClicked)
        self.layout.addWidget(self.table)

        # Кнопка переименовать
        self.btn_rename = QPushButton("Переименовать файлы")
        self.btn_rename.clicked.connect(self.rename_files)
        self.layout.addWidget(self.btn_rename)

        self.folder = None
        self.files = []

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с файлами")
        if not folder:
            return
        self.folder = folder
        self.load_files()

    def load_files(self):
        self.table.setRowCount(0)
        self.files = []

        # ищем md файлы по маске
        for path in glob.glob(os.path.join(self.folder, "*Объявление.md")):
            title = self.extract_title(path)
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(os.path.basename(path)))
            self.table.setItem(row, 1, QTableWidgetItem(title))
            self.files.append(path)

    def extract_title(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # ищем второй заголовок ## ...
            matches = re.findall(r"^##\s+(.*)", content, flags=re.MULTILINE)
            if len(matches) >= 2:
                return matches[1].strip()
        except Exception as e:
            print(f"Ошибка чтения {path}: {e}")
        return ""

    def rename_files(self):
        if not self.files:
            QMessageBox.warning(self, "Внимание", "Сначала выберите папку с файлами.")
            return
        for row, old_path in enumerate(self.files):
            new_name = self.table.item(row, 1).text().strip()
            if not new_name:
                continue
            # Убираем недопустимые символы
            safe_name = re.sub(r"[\\/:*?\"<>|]", "_", new_name) + ".md"
            new_path = os.path.join(self.folder, safe_name)
            old_full_path = old_path
            try:
                if old_full_path != new_path:
                    os.rename(old_full_path, new_path)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось переименовать {old_full_path} -> {new_path}\n{e}")
        QMessageBox.information(self, "Готово", "Файлы переименованы!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
