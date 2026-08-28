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
        self.setCentralWidget(central_widget)

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
        btn_view_attendance.clicked.connect(self.handle_check)

        btn_edit_employee = QPushButton('Edit Employee')
        layout.addWidget(btn_edit_employee)
        btn_edit_employee.clicked.connect(self.handle_edit)

        btn_remove_employee = QPushButton('Remove Employee')
        layout.addWidget(btn_remove_employee)
        btn_remove_employee.clicked.connect(self.handle_del)

    def handle_reg(self):
            dialog = RegisterEmployeeDialog( cur, conn)
            dialog.exec()

    def handle_get(self):
            dialog = FindEmployeeDialog( cur)
            dialog.exec()

    def handle_mark(self):
            dialog = MarkAttendanceDialog( cur, conn)
            dialog.exec()

    def handle_check(self):
            dialog = CheckAttendanceDialog( cur)
            dialog.exec()

    def handle_edit(self):
            dialog = EditEmployeeDialog( cur, conn)
            dialog.exec()

    def handle_del(self):
            dialog = RemoveEmployeeDialog( cur, conn)
            dialog.exec()

class RegisterEmployeeDialog(BaseDialog):
    def __init__(self, cur, conn):
        super().__init__('Register Employee')                     
        self.cur = cur
        self.conn = conn

        self.fname = self.add_field('First Name')
        self.lname = self.add_field('Last Name')
        self.department = self.add_field('Department')
        self.job_title = self.add_field('Job Title')

        btn_save = QPushButton('Save')
        self.layout.addWidget(btn_save)
        btn_save.clicked.connect(self.handle_save)
        btn_save.setDefault(False)
        btn_save.setAutoDefault(False)

    def handle_save(self):
        fname = self.fname.text()
        lname = self.lname.text()
        department = self.department.text()
        job_title = self.job_title.text()
        encoding = register_face()
        if encoding is None:
            QMessageBox.warning(self, 'Error', 'No face detected')
            return
        add_employee(self.cur, self.conn, fname, lname, department, job_title)        

class FindEmployeeDialog(BaseDialog):
    def __init__(self, cur):
        super().__init__('Employee Lookup')
        self.cur = cur

        table = QTableWidget()
        self.layout.addWidget(table)

        cur.execute('SELECT * FROM employees')
        rows = cur.fetchall()

        table.setColumnCount(5)
        table.setRowCount(len(rows))
        table.setHorizontalHeaderLabels(['Full Name', 'Last Name', 'Department', 'Job Title', 'Face'])
        for i, row in enumerate(rows):
             for j, value in enumerate(row):
                  table.setItem(i, j, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()

class MarkAttendanceDialog(BaseDialog):
    def __init__(self,cur, conn):
        super().__init__("Mark Attendance")
        self.cur = cur
        self.conn = conn

        btn_scan = QPushButton('Scan Face')
        btn_scan.clicked.connect(self.handle_scan)
        self.layout.addWidget(btn_scan)

    def handle_scan(self):
        mark_attendance(self.cur , self.conn)
        

class CheckAttendanceDialog(BaseDialog):
    def __init__(self, cur, conn):
        super().__init__("Check Attendance")   
        self.cur = cur

        table = QTableWidget()
        self.layout.addWidget(table)

        cur.execute('SELECT * FROM attendance')
        rows = cur.fetchall()

        table.setColumnCount(4)
        table.setRowCount(len(rows))
        table.setHorizontalHeaderLabels(['Full Name', 'Last Name', 'Department', 'Job Title'])
        for i, row in enumerate(rows):
             for j, value in enumerate(row):
                  table.setItem(i, j, QTableWidgetItem(str(value))) 
        table.resizeColumnsToContents()                                     

class EditEmployeeDialog(BaseDialog):
    def __init__(self, cur, conn):
        super().__init__('Edit Employee Details')
        self.cur = cur
        self.conn = conn

        self.layout.addWidget(QLabel('Employee ID'))
        self.employee_id = QLineEdit()
        self.employee_id.setValidator(QIntValidator())
        self.layout.addWidget(self.employee_id)

        self.column_choice = QComboBox()
        self.column_choice.addItems(['fname', 'lname',' department',' job_title',' face_encoding'])
        self.layout.addWidget(self.column_choice)

        self.layout.addWidget(QLabel('New Value'))
        self.new_value = QLineEdit()
        self.layout.addWidget(self.new_value)

        btn_save = QPushButton('Save')
        btn_save.clicked.connect(self.handle_save)
        self.layout.addWidget(btn_save)
        btn_save.setDefault(False)
        btn_save.setAutoDefault(False)

    def handle_save(self):
        employee_id = self.employee_id.text()
        column = self.column_choice.currentText()
        # new_value = self.new_value.text()

        if column =='face_encoding':
            new_value = register_face()
            if new_value is None:
                QMessageBox.warning(self, 'Error', 'No face detected')
                return
            else:
                new_value = self.new_value.text()

        edit_employee(self.cur, self.conn, employee_id, column, new_value)
        self.employee_id.clear()
        self.new_value.clear()

class RemoveEmployeeDialog(BaseDialog):
    def __init__(self, cur, conn):
        super().__init__('Remove Employee')

        self.cur = cur
        self.conn = conn

        self.layout.addWidget(QLabel('Employee ID'))
        self.employee_id_input = QLineEdit()
        self.employee_id_input.setValidator(QIntValidator())
        self.layout.addWidget(self.employee_id_input)

        btn_save = QPushButton('Save')
        self.layout.addWidget(btn_save)
        btn_save.clicked.connect(self.handle_save)
        btn_save.setDefault(False)
        btn_save.setAutoDefault(False)

    def handle_save(self):
        employee_id = self.employee_id_input.text()

        reply = QMessageBox.question(self, 'Confirm Delete', "Are you sure you want to remove this employee's details? ", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            remove_employee(self.cur, self.conn, employee_id)
            self.employee_id_input.clear()

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())
cur.close()
conn.close()