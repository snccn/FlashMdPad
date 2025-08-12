# coding:utf-8
from PySide6.QtWidgets import QDialog, QLineEdit, QHBoxLayout, QPushButton, QLabel

class FindDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("查找")
        self.setFixedWidth(300)
        layout = QHBoxLayout(self)
        self.label = QLabel("查找内容:")
        self.line_edit = QLineEdit()
        self.find_btn = QPushButton("查找下一个")
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.find_btn)
        self.find_btn.clicked.connect(self.accept)

    def get_text(self):
        return self.line_edit.text()