from PyQt5.QtWidgets import QFileDialog, QMessageBox

class PyNoteOperations:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def open_file(self, parent):
        filename, _ = QFileDialog.getOpenFileName(parent, "Open File", "", "Text Files (*.txt)")
        if filename:
            with open(filename, "r") as file:
                self.text_edit.setText(file.read())

    def save_file(self, parent):
        filename, _ = QFileDialog.getSaveFileName(parent, "Save File", "", "Text Files (*.txt)")
        if filename:
            with open(filename, "w") as file:
                file.write(self.text_edit.toPlainText())
            QMessageBox.information(parent, "File Saved", "File saved successfully.")
