import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction,
    QFileDialog, QMessageBox, QLabel
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Note Taking App")
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        self.text_edit.textChanged.connect(self.update_character_count)
        self.character_count_label = QLabel("Characters: 0", self)
        self.statusBar().addWidget(self.character_count_label)

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
