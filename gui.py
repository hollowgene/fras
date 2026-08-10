import sys
from app import cur, conn, add_employee, get_employee, edit_employee, remove_employee, add_attendance, get_attendance, edit_attendance, remove_attendance, register_face, mark_attendance
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QDialog, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QComboBox, QMessageBox
from PyQt6.QtGui import QIntValidator

class BaseDialog(QDialog):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def add_field(self, label):
        self.layout.addWidget(QLabel(label))
        field = QLineEdit()
        self.layout.addWidget(field)
        return field

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FRAS')
        self.setMinimumSize(1000,800)

        central_widget = QWidget()
        self.centralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        btn_register_employee = QPushButton('Employee Registration')
        layout.addWidget(btn_register_employee)
        btn_register_employee.clicked.connect(self.handle_reg)

        btn_view_employee = QPushButton('Employee Lookup')
        layout.addWidget(btn_view_employee)
        btn_view_employee.clicked.connect(self.handle_get)

        btn_mark_attendance = QPushButton('Mark Attendance')
        layout.addWidget(btn_mark_attendance)
        btn_mark_attendance.clicked.connect(self.handle_mark)

        btn_view_attendance = QPushButton('Check Attendance')
        layout.addWidget(btn_view_attendance)
        btn_view_attendance.clicked.connect(self.handle_get)

        btn_edit_employee = QPushButton('Employee Lookup')
        layout.addWidget(btn_edit_employee)
        btn_edit_employee.clicked.connect(self.handle_get)        