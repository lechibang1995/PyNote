import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QLabel, QMessageBox
from PyNoteOperations import PyNoteOperations

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.text_edited = False

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
        self.text_edit.textChanged.connect(self.set_text_edited)

    def set_text_edited(self):
        self.text_edited = True

    def create_status_bar(self):
        self.character_count_label = QLabel("Characters: 0", self)
        self.statusBar().addWidget(self.character_count_label)

    def create_menu_bar(self):
        file_menu = self.menuBar().addMenu("&File")

        new_action = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_note)
        file_menu.addAction(new_action)

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

    def new_note(self):
        new_window = MainWindow()
        new_window.show()
        app.open_windows.append(new_window)

    def open_file(self):
        self.file_operations.open_file(self)

    def save_file(self):
        if self.file_operations.save_file(self):
            self.text_edited = False

    def close_file(self):
        if self.confirm_save_changes():
            QApplication.quit()

    def closeEvent(self, event):
        if self.confirm_save_changes():
            event.accept()
        else:
            event.ignore()

    def confirm_save_changes(self):
        if not self.text_edit.toPlainText() or not self.text_edited:
            return True

        response = QMessageBox().question(self, "", "Do you want to save your changes?",
                                          QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        if response == QMessageBox.Save:
            self.save_file()
            return True
        elif response == QMessageBox.Discard:
            return True
        else:
            return False
        
    def reset_text_edited(self):
        self.text_edited = False

    def update_character_count(self):
        character_count = len(self.text_edit.toPlainText())
        self.character_count_label.setText(f"Characters: {character_count}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.open_windows = []
    window = MainWindow()
    app.open_windows.append(window)
    window.show()
    sys.exit(app.exec_())

