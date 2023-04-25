import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction,
    QFileDialog, QMessageBox, QLabel
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Note Taking App")
        self.create_text_edit()
        self.create_status_bar()
        self.create_menu_bar()

    def create_text_edit(self):
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        self.text_edit.textChanged.connect(self.update_character_count)

    def create_status_bar(self):
        self.character_count_label = QLabel("Characters: 0", self)
        self.statusBar().addWidget(self.character_count_label)

    def create_menu_bar(self):
        file_menu = self.menuBar().addMenu("&File")

        open_action = self.create_action("&Open", "Ctrl+O", self.open_file)
        file_menu.addAction(open_action)

        save_action = self.create_action("&Save", "Ctrl+S", self.save_file)
        file_menu.addAction(save_action)

        close_action = self.create_action("&Close", "Ctrl+W", self.close_file)
        file_menu.addAction(close_action)

    def create_action(self, text, shortcut, triggered_function):
        action = QAction(text, self)
        action.setShortcut(shortcut)
        action.triggered.connect(triggered_function)
        return action

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
        if filename:
            with open(filename, "r") as file:
                self.text_edit.setText(file.read())

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")
        if filename:
            with open(filename, "w") as file:
                file.write(self.text_edit.toPlainText())
            QMessageBox.information(self, "File Saved", "File saved successfully.")

    def close_file(self):
        if not self.text_edit.toPlainText():
            QApplication.quit()
            return

        response = self.show_save_changes_message_box()
        if response == QMessageBox.Save:
            self.save_file()
        elif response != QMessageBox.Cancel:
            QApplication.quit()

    def closeEvent(self, event):
        if not self.text_edit.toPlainText():
            event.accept()
            return

        response = self.show_save_changes_message_box()
        if response == QMessageBox.Save:
            self.save_file()
        elif response == QMessageBox.Cancel:
            event.ignore()
        else:
            event.accept()

    def show_save_changes_message_box(self):
        message_box = QMessageBox()
        message_box.setText("Do you want to save your changes?")
        message_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        message_box.setDefaultButton(QMessageBox.Save)
        return message_box.exec_()

    def update_character_count(self):
        character_count = len(self.text_edit.toPlainText())
        self.character_count_label.setText(f"Characters: {character_count}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
