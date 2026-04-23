"""
explain.py — A plain-English walkthrough of how this backend is built.

Run it with:
    python explain.py

No server needed. No database needed. Just Python.
"""

# ==============================================================================
# PART 1 — WHAT IS A CLASS?
# ==============================================================================
#
# A class is a blueprint. You define it once, then create as many objects
# from it as you want. Each object gets its own copy of the data (attributes).
#
# Think of it like a form: the class is the blank form, an instance is a
# filled-in form.

print("=" * 60)
print("PART 1 — What is a class?")
print("=" * 60)

# Here is the simplest possible class — just a blueprint with two fields.
class Teacher:
    def __init__(self, name, subject):
        # __init__ runs automatically when you create a new Teacher.
        # `self` means "the object being created right now".
        self.name    = name
        self.subject = subject

    def introduce(self):
        # A method is a function that belongs to the class.
        # Every method receives `self` so it can access the object's data.
        return f"Hi, I'm {self.name} and I teach {self.subject}."

    def __repr__(self):
        # __repr__ controls what you see when you print the object.
        return f"Teacher(name={self.name!r}, subject={self.subject!r})"


# Create two Teacher objects from the same blueprint.
teacher1 = Teacher(name="Alice Martin", subject="Mathematics")
teacher2 = Teacher(name="Bob Johnson",  subject="Physics")

print("\nCreating two teachers from the Teacher class:")
print("  teacher1 =", teacher1)          # calls __repr__
print("  teacher2 =", teacher2)

print("\nAccessing individual fields:")
print("  teacher1.name    =", teacher1.name)
print("  teacher1.subject =", teacher1.subject)

print("\nCalling a method on teacher1:")
print(" ", teacher1.introduce())

print("\nKey point: teacher1 and teacher2 are SEPARATE objects.")
print("  Changing one does NOT affect the other.")
teacher1.subject = "Advanced Mathematics"
print("  After teacher1.subject = 'Advanced Mathematics':")
print("  teacher1.subject =", teacher1.subject)
print("  teacher2.subject =", teacher2.subject, "  ← untouched")


# ==============================================================================
# PART 2 — CLASSES WITH RELATIONSHIPS (Course belongs to a Teacher)
# ==============================================================================
#
# Real data has connections. A course is always taught by a teacher.
# We represent that by storing the teacher object inside the course.

print("\n" + "=" * 60)
print("PART 2 — Classes with relationships")
print("=" * 60)

class Course:
    def __init__(self, name, teacher):
        self.name    = name
        self.teacher = teacher  # store the whole Teacher object here

    def __repr__(self):
        return f"Course(name={self.name!r}, teacher={self.teacher.name!r})"


# Reset teacher1 back for clarity
teacher1 = Teacher(name="Alice Martin", subject="Mathematics")

course1 = Course(name="Calculus 101",    teacher=teacher1)
course2 = Course(name="Algebra Advanced", teacher=teacher1)  # same teacher, two courses

print("\nCreating two courses, both taught by Alice:")
print("  course1 =", course1)
print("  course2 =", course2)

print("\nAccessing the teacher through the course:")
print("  course1.teacher       =", course1.teacher)
print("  course1.teacher.name  =", course1.teacher.name)
print("  course1.teacher.subject =", course1.teacher.subject)

print("\nThis is the same object — not a copy:")
print("  course1.teacher is teacher1 →", course1.teacher is teacher1)


# ==============================================================================
# PART 3 — THREE LEVELS: Teacher → Course → Student
# ==============================================================================
#
# The full chain:  Teacher teaches Courses,  Students enrol in a Course.

print("\n" + "=" * 60)
print("PART 3 — Three levels: Teacher → Course → Student")
print("=" * 60)

class Student:
    def __init__(self, name, age, course):
        self.name   = name
        self.age    = age
        self.course = course  # which course this student is in

    def __repr__(self):
        return (
            f"Student(name={self.name!r}, age={self.age}, "
            f"course={self.course.name!r})"
        )

    def describe(self):
        return (
            f"{self.name} (age {self.age}) is enrolled in "
            f"'{self.course.name}', taught by {self.course.teacher.name}."
        )


student1 = Student(name="Diana Prince", age=20, course=course1)
student2 = Student(name="Ethan Hunt",   age=22, course=course1)
student3 = Student(name="Fiona Green",  age=19, course=course2)

print("\nCreating students:")
print("  student1 =", student1)
print("  student2 =", student2)
print("  student3 =", student3)

print("\nNavigating the full chain from a student:")
print(" ", student1.describe())
print(" ", student3.describe())

print("\nYou can chain attribute access as deep as you want:")
print("  student1.course.teacher.name =", student1.course.teacher.name)
print("  student1.course.teacher.subject =", student1.course.teacher.subject)


# ==============================================================================
# PART 4 — LISTS AND LOOPS
# ==============================================================================
#
# Usually you have many students. Store them in a list, then loop over it.

print("\n" + "=" * 60)
print("PART 4 — Lists and loops")
print("=" * 60)

all_students = [student1, student2, student3]

print("\nAll students:")
for student in all_students:
    print("  -", student)

print("\nOnly students in Calculus 101:")
for student in all_students:
    if student.course.name == "Calculus 101":
        print("  -", student.name)

print("\nAll students, sorted by age:")
sorted_students = sorted(all_students, key=lambda s: s.age)
for student in sorted_students:
    print(f"  age {student.age} — {student.name}")


# ==============================================================================
# PART 5 — DICTIONARIES (how the API sends data over the network)
# ==============================================================================
#
# Objects can't travel over the internet — JSON can.
# We convert an object to a plain dictionary before sending it.
# This is what the `TeacherOut` Pydantic schema does in the real API.

print("\n" + "=" * 60)
print("PART 5 — Dictionaries: from objects to JSON")
print("=" * 60)

print("\nA Python dictionary is key → value pairs:")
teacher_dict = {"id": 1, "name": "Alice Martin", "subject": "Mathematics"}
print("  teacher_dict =", teacher_dict)
print("  teacher_dict['name'] =", teacher_dict["name"])

print("\nConverting a Teacher object to a dictionary (what the API does):")
def teacher_to_dict(teacher, id):
    return {"id": id, "name": teacher.name, "subject": teacher.subject}

print("  teacher_to_dict(teacher1, id=1) =", teacher_to_dict(teacher1, id=1))

print("\nConverting a Student object — including its linked course and teacher:")
def student_to_dict(student, id):
    return {
        "id":        id,
        "name":      student.name,
        "age":       student.age,
        "course":    student.course.name,
        "teacher":   student.course.teacher.name,
    }

print("  student_to_dict(student1, id=1) =", student_to_dict(student1, id=1))


# ==============================================================================
# PART 6 — FUNCTIONS THAT DO DATABASE WORK (what the services do)
# ==============================================================================
#
# In the real API, a "service" is a class with methods that run SQL queries.
# Here we simulate that with a plain list acting as the database.

print("\n" + "=" * 60)
print("PART 6 — Service functions (like the real TeacherService)")
print("=" * 60)

# Pretend this list IS the database table.
fake_db = [
    {"id": 1, "name": "Alice Martin", "subject": "Mathematics"},
    {"id": 2, "name": "Bob Johnson",  "subject": "Physics"},
    {"id": 3, "name": "Carol Smith",  "subject": "Biology"},
]

def list_all_teachers():
    # In the real service: SELECT id, name, subject FROM teachers
    return fake_db

def get_teacher(teacher_id):
    # In the real service: SELECT ... FROM teachers WHERE id = :id
    for row in fake_db:
        if row["id"] == teacher_id:
            return row
    return None  # not found

def create_teacher(name, subject):
    # In the real service: INSERT INTO teachers (name, subject) VALUES (...)
    new_id = max(row["id"] for row in fake_db) + 1
    new_teacher = {"id": new_id, "name": name, "subject": subject}
    fake_db.append(new_teacher)
    return new_teacher

def update_teacher(teacher_id, new_subject):
    # In the real service: UPDATE teachers SET subject = :subject WHERE id = :id
    teacher = get_teacher(teacher_id)
    if teacher is None:
        return None
    teacher["subject"] = new_subject
    return teacher

def delete_teacher(teacher_id):
    # In the real service: DELETE FROM teachers WHERE id = :id
    teacher = get_teacher(teacher_id)
    if teacher is None:
        return False
    fake_db.remove(teacher)
    return True


print("\nlist_all_teachers():")
for t in list_all_teachers():
    print("  ", t)

print("\nget_teacher(2):", get_teacher(2))
print("get_teacher(99):", get_teacher(99), " ← None means not found")

print("\ncreate_teacher('Diana Teach', 'History'):", create_teacher("Diana Teach", "History"))
print("list_all_teachers() after insert:")
for t in list_all_teachers():
    print("  ", t)

print("\nupdate_teacher(1, 'Advanced Calculus'):", update_teacher(1, "Advanced Calculus"))
print("get_teacher(1) now:", get_teacher(1))

print("\ndelete_teacher(4):", delete_teacher(4))
print("list_all_teachers() after delete:")
for t in list_all_teachers():
    print("  ", t)


# ==============================================================================
# PART 7 — THE REAL SQL (what actually runs in the backend)
# ==============================================================================
#
# The service files use SQLAlchemy's `text()` to run plain SQL strings.
# Here we show what those strings look like and what they mean.

print("\n" + "=" * 60)
print("PART 7 — The real SQL statements (plain text)")
print("=" * 60)

sql_examples = {
    "List all teachers": (
        "SELECT id, name, subject FROM teachers"
    ),
    "Get one teacher by id": (
        "SELECT id, name, subject FROM teachers WHERE id = :id"
        "\n            -- :id is a placeholder, filled in safely at runtime"
    ),
    "Create a teacher": (
        "INSERT INTO teachers (name, subject) VALUES (:name, :subject)"
        "\n            -- values come from the JSON the client sent"
    ),
    "Update a teacher's subject": (
        "UPDATE teachers SET subject = :subject WHERE id = :id"
        "\n            -- only the rows with this id are touched"
    ),
    "Delete a teacher": (
        "DELETE FROM teachers WHERE id = :id"
        "\n            -- cascade rule in the DB also deletes their courses"
    ),
}

for description, sql in sql_examples.items():
    print(f"\n  [{description}]")
    print(f"    {sql}")


# ==============================================================================
# SUMMARY
# ==============================================================================

print("\n" + "=" * 60)
print("SUMMARY — How the pieces fit together")
print("=" * 60)
print("""
  1. CLASS       — a blueprint for an object (Teacher, Course, Student).
                   Each instance holds its own data in attributes (self.name).

  2. METHOD      — a function inside a class (__init__, introduce, __repr__).
                   It always receives `self` as the first argument.

  3. RELATIONSHIP — one object holds another as an attribute (course.teacher).
                    This mirrors a foreign key in the database.

  4. LIST        — store many objects together; loop with `for`.

  5. DICTIONARY  — key/value pairs {"id": 1, "name": "Alice"}.
                   This is what JSON looks like once Python parses it.

  6. SERVICE     — a class whose methods run SQL queries (list, get,
                   create, update, delete). Routes call the service;
                   the service talks to the database.

  7. SQL         — the actual language the database understands.
                   SELECT fetches rows, INSERT adds one, UPDATE changes
                   fields, DELETE removes. :placeholders keep it safe.
""")
