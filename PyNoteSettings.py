from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox
from PyQt5.QtCore import Qt

class PyNoteSettings(QDialog):
    def __init__(self, parent=None):
        super(PyNoteSettings, self).__init__(parent)

        self.setWindowTitle("Settings")

        layout = QVBoxLayout()

        self.ui_scale_label = QLabel("UI Scale:")
        layout.addWidget(self.ui_scale_label)

        self.ui_scale_combo = QComboBox()
        self.ui_scale_combo.addItem("100")
        self.ui_scale_combo.addItem("110")
        self.ui_scale_combo.addItem("125")
        self.ui_scale_combo.addItem("150")
        self.ui_scale_combo.addItem("175")
        layout.addWidget(self.ui_scale_combo)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def ui_scale(self):
        return int(self.ui_scale_combo.currentText()) / 100

    @staticmethod
    def get_settings(parent=None):
        dialog = PyNoteSettings(parent)
        result = dialog.exec_()
        scale = dialog.ui_scale()
        return (scale, result == QDialog.Accepted)
