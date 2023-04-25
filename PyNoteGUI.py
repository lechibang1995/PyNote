import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QLabel, QMessageBox
from PyNoteOperations import PyNoteOperations

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Note Taking App")
        self.create_text_edit()
        self.create_status_bar()
        self.create_menu_bar()

        self.file_operations = PyNoteOperations(self.text_edit)

    def create_text_edit(self):
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        self.text_edit.textChanged.connect(self.update_character_count)

    def create_status_bar(self):
        self.character_count_label = QLabel("Characters: 0", self)
        self.statusBar().addWidget(self.character_count_label)

    def create_menu_bar(self):
        file_menu = self.menuBar().addMenu("&File")

        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        close_action = QAction("&Close", self)
        close_action.setShortcut("Ctrl+W")
        close_action.triggered.connect(self.close_file)
        file_menu.addAction(close_action)

    def open_file(self):
        self.file_operations.open_file(self)

    def save_file(self):
        self.file_operations.save_file(self)

    def close_file(self):
        if not self.text_edit.toPlainText():
            QApplication.quit()
            return

        response = QMessageBox().question(self, "", "Do you want to save your changes?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        if response == QMessageBox.Save:
            self.save_file()
        elif response != QMessageBox.Cancel:
            QApplication.quit()

    def closeEvent(self, event):
        if not self.text_edit.toPlainText():
            event.accept()
            return

        response = QMessageBox().question(self, "", "Do you want to save your changes?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        if response == QMessageBox.Save:
            self.save_file()
        elif response == QMessageBox.Cancel:
            event.ignore()
        else:
            event.accept()

    def update_character_count(self):
        character_count = len(self.text_edit.toPlainText())
        self.character_count_label.setText(f"Characters: {character_count}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
