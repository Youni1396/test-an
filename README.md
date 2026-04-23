# School API

A teaching backend built with **FastAPI + SQLAlchemy + SQLite**. It manages teachers, courses, students, and grades through a REST API. There is no frontend on purpose — the goal is to understand how a server and database work before adding more moving parts.

---

## Prerequisites

- Python 3.10 or later
- No other software needed (SQLite is bundled with Python)

---

## Quickstart

```bash
cd backend

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Mac / Linux
# .venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Start the development server
uvicorn app.main:app --reload --port 1234
```

Open **http://127.0.0.1:1234/docs** — FastAPI generates an interactive UI for every endpoint. You can test all routes from that page without writing any code.

---

## Running the tests

```bash
# (make sure the virtual environment is activated)
pytest
```

Tests run against an in-memory database and do not touch `school.db`.

---

## Project structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app entry point, router registration
│   ├── database.py      # SQLAlchemy engine, session factory, Base
│   ├── models/          # ORM table definitions (Teacher, Course, Student, Grade)
│   ├── schemas/         # Pydantic request/response shapes
│   ├── routes/          # HTTP endpoint handlers (thin — delegate to services)
│   └── services/        # Business logic and SQL queries
├── tests/               # pytest test suite (in-memory DB)
├── requirements.txt
├── diagram.md           # Database schema diagram
└── README.md            # Full learning guide
```

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/teachers` | List all teachers |
| POST | `/teachers` | Create a teacher |
| GET | `/teachers/{id}` | Get one teacher |
| PATCH | `/teachers/{id}` | Update a teacher |
| DELETE | `/teachers/{id}` | Delete a teacher |
| GET | `/courses` | List all courses |
| POST | `/courses` | Create a course |
| GET | `/courses/{id}` | Get one course |
| PATCH | `/courses/{id}` | Update a course |
| DELETE | `/courses/{id}` | Delete a course |
| GET | `/students` | List all students |
| POST | `/students` | Create a student |
| GET | `/students/{id}` | Get one student |
| PATCH | `/students/{id}` | Update a student |
| DELETE | `/students/{id}` | Delete a student |
| GET | `/grades` | List all grades |
| POST | `/grades` | Create a grade |
| GET | `/grades/{id}` | Get one grade |
| PATCH | `/grades/{id}` | Update a grade |
| DELETE | `/grades/{id}` | Delete a grade |

---

## Database relationships

```
Teachers
  └── Courses  (teacher_id → teachers.id)
        └── Students  (course_id → courses.id)
              └── Grades  (student_id → students.id)
```

Deleting a teacher cascades through courses → students → grades automatically.

---

## Learning guide

See [`backend/README.md`](backend/README.md) for the full walkthrough: how HTTP works, how SQLAlchemy connects to the database, what each layer does, and how to complete the grades exercise.
