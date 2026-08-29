import face_recognition
import cv2
from PyQt6.QtWidgets import QApplication
import psycopg2
import os
import pickle
from datetime import datetime, date
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / '.env')

try:
    conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
    )
    cur= conn.cursor()
    print('Connected to Database successfully')
except psycopg2.OperationalError as e:
    print(f'Something went wrong: {e}')

def run_query(cur, conn, query, params=None):
    cur.execute(query, params)
    conn.commit()

def add_employee(cur, conn, fname, lname, department, job_title, face_encoding):
    run_query(cur, conn, '''INSERT INTO employees
        (fname, lname, department, job_title, face_encoding)
        VALUES ( %s, %s, %s, %s, %s)''',
        (fname, lname, department, job_title, face_encoding)
    )
    print('Row Inserted')

def get_employee(cur):
    cur.execute('SELECT * FROM public.employees')
    return cur.fetchall()

def edit_employee(cur, conn, employee_id, column, new_value):
    run_query(cur, conn, f'UPDATE employees SET {column} = %s WHERE employee_id = %s', (new_value, employee_id))
def remove_employee(cur, conn, employee_id):
    run_query(cur, conn, f'DELETE FROM employees WHERE employee_id = %s', (employee_id,))

def add_attendance(cur, conn,employee_id, login_date, time_in, time_out, duration, status):
    run_query(cur, conn, '''INSERT INTO attendance
        (employee_id, login_date, time_in, time_out, duration, status)
        VALUES (%s, %s, %s, %s, %s, %s)''',
        ( employee_id, login_date, time_in, time_out, duration, status)
    )
    print('Row Inserted')

def get_attendance(cur):
    cur.execute('SELECT * FROM public.attendance')
    return cur.fetchall()

def edit_attendance(cur, conn, attendance_id, column, new_value):
    run_query(cur, conn, f'UPDATE attendance SET {column} = %s WHERE attendance_id = %s', (new_value, attendance_id))

def remove_attendance(cur, conn, attendance_id):
    run_query(cur, conn, f'DELETE FROM attendance WHERE attendance_id = %s', (attendance_id,))

def register_face():
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    capture.release()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_frame)

    if  len(encodings) == 0:
        print('No face detected')
        return None
    
    encoding_bytes = pickle.dumps(encodings[0])
    return encoding_bytes

# def recognize_face(stored_encoding):
#     capture = cv2.VideoCapture(0)
#     ret, frame = capture.read()
#     capture.release()

#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     encodings = face_recognition.face_encodings(rgb_frame)

#     if  len(encodings) == 0:
#         return False

#     results = face_recognition.compare_faces([stored_encoding], encodings[0])
#     return results[0]

def mark_attendance(cur, conn):
    employees = get_employee(cur)

    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    capture.release()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_frame)

    stored_encodings = []
    names = []
    for employee in employees:
        stored_encodings.append(pickle.loads(employee[5]))
        names.append(employee[1])

    if len(encodings) == 0:
        print('No face detected')
        return

    results = face_recognition.compare_faces(stored_encodings, encodings[0])

    login_date = date.today()
    time_in = datetime.now()

    if True in results:
        match_index = results.index(True)
        matched_employee_id = employees[match_index][0]
        matched_name = names[match_index]
        print(f'Recognized: {matched_name}')
        add_attendance(cur, conn, matched_employee_id, login_date, time_in, None, None, None)
    else:
        print('Face not recognized')    

# encoding = register_face()
# if encoding is None:
#     print('No face detected, registeration failed')
# else:
#     add_employee(cur, conn, 'unfair', 'mate', 'HR', 'Interviewer', encoding)
#     print('Employee Registered!')
#     mark_attendance(cur, conn)

#venv\Scripts\activate