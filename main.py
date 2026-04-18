import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        self.connect()
        if not self.connection:
            raise Exception("Database connection is not established.")
        
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
        data = cursor.fetchall()
        self.close()
        return data
    


    db = DatabaseManager('students.db')
    while True:
        print("0. Вихід")
        print("1. Показати всіх студентів")
        print("2. Показати всі курси")
        print("3. Додати студента")
        print("4. Додати курс")
        print("5. Записати студента на курс")
        print("6. Показати курси студента")
        print("7. Показати студентів курсу")
            
    
        choice = input("Виберіть дію: ")
        if choice == '0':
            break
        if choice == '1':
            students = db.execute_query("SELECT * FROM students")
            for student in students:
                print(student)
        elif choice == '2':
            courses = db.execute_query("SELECT * FROM courses")
            for course in courses:
                print(course)
        elif choice == '3':
            name = input("Введіть ім'я студента: ")
            db.execute_query("INSERT INTO students (name) VALUES (?)", (name,))
        elif choice == '4':
            title = input("Введіть назву курсу: ")
            db.execute_query("INSERT INTO courses (title) VALUES (?)", (title,))
        elif choice == '5':
            student_id = input("Введіть ID студента: ")
            course_id = input("Введіть ID курсу: ")
            db.execute_query("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
        elif choice == '6': 
            student_id = input("Введіть ID студента: ")
            courses = db.execute_query("""
                SELECT c.title FROM courses c
                JOIN student_courses sc ON c.course_id = sc.course_id
                WHERE sc.student_id = ?
            """, (student_id,))
            for course in courses:
                print(course[0])
        elif choice == '7':
            course_id = input("Введіть ID курсу: ")
            students = db.execute_query("""
                SELECT s.name FROM students s
                JOIN student_courses sc ON s.student_id = sc.student_id
                WHERE sc.course_id = ?
            """, (course_id,))
            for student in students:
                print(student[0])
                