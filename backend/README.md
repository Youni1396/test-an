# School API — Backend Learning Guide

This project is a teaching backend. It manages teachers, courses, students, and grades
through a REST API backed by a real database. There is no frontend on purpose — the goal
is to understand how a server works before adding more moving parts.

This document explains everything from scratch: what a backend actually is, how the
database lives on your computer, how the two talk to each other, what every file in this
repo does, and how to complete the exercise at the end.

---

## Table of Contents

1. [What is a backend?](#1-what-is-a-backend)
2. [How does HTTP work?](#2-how-does-http-work)
3. [HTTP status codes](#3-http-status-codes)
4. [What is a database and where does it live?](#4-what-is-a-database-and-where-does-it-live)
5. [How does the backend talk to the database?](#5-how-does-the-backend-talk-to-the-database)
6. [The four layers of this app](#6-the-four-layers-of-this-app)
7. [File-by-file walkthrough](#7-file-by-file-walkthrough)
8. [How the server starts up](#8-how-the-server-starts-up)
9. [What happens on a single request](#9-what-happens-on-a-single-request)
10. [The database relationships](#10-the-database-relationships)
11. [Running the project](#11-running-the-project)
12. [How to read the repo and complete the exercise](#12-how-to-read-the-repo-and-complete-the-exercise)

---

## 1. What is a backend?

Imagine a restaurant. The customer (frontend) looks at a menu and places an order. The
waiter (the API) takes that order to the kitchen. The kitchen (the backend) decides how to
make the food, checks whether the ingredient exists, cooks it, and hands the result back
to the waiter, who brings it to the customer.

In software terms:

```
Browser / mobile app          Backend (this project)         Database
─────────────────────         ──────────────────────         ────────
"Show me all students"   -->  receives the request      -->  SELECT * FROM students
                         <--  returns JSON list          <--  [row, row, row]
```

The backend is the program running on a server (or your laptop, during development) that:

- Listens for incoming HTTP requests on a port (like `8000`)
- Decides what to do with each request (which function to call)
- Reads or writes to the database as needed
- Sends a response back (usually JSON)

The backend is the place where **rules live**. A frontend can be hacked by any user — the
browser just runs JavaScript that anyone can edit. The backend is the authority. If a
student must belong to a course that actually exists, the backend enforces that check
before touching the database. The frontend cannot bypass it.

---

## 2. How does HTTP work?

HTTP (HyperText Transfer Protocol) is just a text format that computers agreed to use when
talking over a network. Every request has:

- **A method** — the verb that says what kind of action this is
- **A path** — the address of the resource being acted on
- **Headers** — metadata (content type, auth tokens, etc.)
- **A body** — optional data sent along (usually JSON for APIs)

The five methods you will use in this project:

| Method | Meaning | Used for |
|--------|---------|---------|
| GET | "give me data" | Fetching one record or a list |
| POST | "create something new" | Creating a resource |
| PATCH | "partially update something" | Changing a few fields without rewriting everything |
| PUT | "replace something entirely" | Full replacement (not used here) |
| DELETE | "remove this" | Deleting a record |

A GET request never has a body — the parameters go in the URL (e.g., `/students/3`).
A POST or PATCH request carries a JSON body describing what to create or change.

---

## 3. HTTP status codes

Every HTTP response comes with a three-digit **status code** that tells the caller what
happened. You have seen these in browser DevTools or when a website says "404 Not Found."

They are grouped by their first digit:

| Range | Category | Meaning |
|-------|----------|---------|
| 2xx | Success | The request worked |
| 3xx | Redirect | Go look somewhere else |
| 4xx | Client error | You (the caller) did something wrong |
| 5xx | Server error | We (the server) broke something |

The specific codes this project uses:

| Code | Name | When it is sent |
|------|------|----------------|
| **200** OK | The default success | GET requests that return data |
| **201** Created | A new resource was made | Successful POST |
| **204** No Content | Success, nothing to return | Successful DELETE |
| **400** Bad Request | The request data is invalid | e.g. referencing a course that does not exist |
| **404** Not Found | The resource does not exist | GET/PATCH/DELETE for an ID that is not in the DB |
| **422** Unprocessable Entity | JSON shape is wrong | Sent automatically by FastAPI when required fields are missing |
| **500** Internal Server Error | Unhandled exception in the server | A bug we did not catch |

When you write a route, you are deciding: "what code does this action return on success,
and what code do I return when something goes wrong?" The comments in `routes/grades.py`
tell you exactly which codes to use.

---

## 4. What is a database and where does it live?

A database is a program whose entire job is to store data reliably and let you query it
quickly. It stores data in **tables** — think of them like spreadsheets with strict column
types.

```
students table
┌────┬────────┬─────┬───────────┐
│ id │  name  │ age │ course_id │
├────┼────────┼─────┼───────────┤
│  1 │ Alice  │ 17  │     1     │
│  2 │ Bob    │ 16  │     1     │
│  3 │ Carlos │ 18  │     2     │
└────┴────────┴─────┴───────────┘
```

This project uses **SQLite**, the simplest database that exists. Unlike PostgreSQL or
MySQL, SQLite does not run as a separate program. It is just a single file on disk:
`backend/school.db`. When the backend writes to the database, it is literally writing
bytes into that file. When it reads, it reads from that file.

You can open that file directly with any SQLite browser (e.g., "DB Browser for SQLite",
a free download) and see every row in every table.

In production apps, the database is usually a separate program (PostgreSQL, MySQL) running
on a different machine or container. But the code in this project would barely change —
only the connection string in `database.py` would be different. That is why we abstract it.

**Why a separate program at all?**

- Databases are optimized for reading and writing data at scale
- They handle concurrent access safely (two requests writing at the same time)
- They enforce constraints (a student cannot have a `course_id` pointing to a course that
  does not exist)
- They survive crashes — data is durably written to disk

---

## 5. How does the backend talk to the database?

The backend does not write SQL strings manually and send them over a socket (though it
could). Instead it uses two abstraction layers:

### Layer 1: The database driver

Python has a low-level library called `sqlite3` (built in) that opens a connection to the
SQLite file and sends raw SQL strings like:

```sql
SELECT id, name, age, course_id FROM students WHERE id = 3;
```

### Layer 2: SQLAlchemy (the ORM)

An **ORM** (Object-Relational Mapper) lets you work with Python objects instead of SQL
strings. You define a class (`Student`) and SQLAlchemy translates operations on that class
into the correct SQL for whatever database you are using.

In `database.py` we set this up in three steps:

```python
# 1. The engine: one connection pool for the whole app
engine = create_engine("sqlite:///./school.db")

# 2. The session factory: creates individual "conversations" with the DB
SessionLocal = sessionmaker(bind=engine)

# 3. The base class: all model classes inherit from this,
#    so SQLAlchemy knows which classes represent tables
class Base(DeclarativeBase):
    pass
```

Each incoming HTTP request gets its own **session** — a temporary, isolated conversation
with the database. The session collects operations (inserts, updates) and can commit or
roll back all of them at once. After the request is done, the session is closed and the
connection goes back to the pool.

This is why every route function has this parameter:

```python
db: Session = Depends(get_db)
```

FastAPI calls `get_db()` before the route runs, gets a session, passes it to the route,
and closes it after the route returns. The route never has to worry about opening or
closing connections.

### How a query actually travels

When a service calls:

```python
self.db.execute(text("SELECT id, name FROM students WHERE id = :id"), {"id": 3})
```

The journey looks like this:

```
service method
    │
    ▼
SQLAlchemy session
    │  wraps the call in a transaction
    ▼
SQLAlchemy engine
    │  picks a connection from the pool
    ▼
sqlite3 driver
    │  sends bytes over a file descriptor to the SQLite file
    ▼
school.db (the file on disk)
    │  reads pages, finds the row, returns it
    ▲
    │
sqlite3 driver
    │  deserializes the bytes into Python tuples
    ▲
    │
SQLAlchemy session
    │  hands back a Row object
    ▲
    │
service method
    │  converts the Row to a dict and returns it
    ▲
    │
route function
    │  FastAPI serializes the dict to JSON
    ▲
    │
HTTP response to the client
```

---

## 6. The four layers of this app

Every backend worth understanding has separation of concerns. Each layer has exactly one
job. If you need to fix a bug, you know which file to open.

```
HTTP request comes in
        │
        ▼
┌───────────────────────────────────────┐
│  ROUTES  (routes/*.py)                │
│  "What HTTP path/method maps to what" │
│  - parse URL params and JSON body     │
│  - call the right service method      │
│  - choose the right status code       │
└───────────────────┬───────────────────┘
                    │ calls
                    ▼
┌───────────────────────────────────────┐
│  SERVICES  (services/*.py)            │
│  "What are the business rules"        │
│  - validate that foreign keys exist   │
│  - decide what SQL to run             │
│  - commit or roll back transactions   │
└───────────────────┬───────────────────┘
                    │ uses
                    ▼
┌───────────────────────────────────────┐
│  MODELS  (models/*.py)                │
│  "What does the database look like"   │
│  - define tables and columns          │
│  - define foreign keys and relations  │
└───────────────────────────────────────┘
        +
┌───────────────────────────────────────┐
│  SCHEMAS  (schemas/*.py)              │
│  "What does the JSON look like"       │
│  - validate incoming request bodies   │
│  - define the shape of responses      │
└───────────────────────────────────────┘
```

---

## 7. File-by-file walkthrough

### `app/main.py`

The entry point. This is the only file that knows about every other file. It:

1. Creates the FastAPI application object
2. Calls `Base.metadata.create_all()` to create any tables that do not exist yet
3. Registers each router (teachers, courses, students, grades) under the app

You never put business logic or SQL here. Its job is wiring.

### `app/database.py`

Everything related to the database connection lives here. The three objects it exports
(`engine`, `SessionLocal`, `Base`) are imported by models and routes throughout the app.
Change only this file if you ever want to swap SQLite for PostgreSQL.

### `app/models/`

Each file defines one SQLAlchemy model — a Python class that maps to a table.

```python
class Student(Base):
    __tablename__ = "students"         # ← the actual table name in SQL

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)

    course = relationship("Course", back_populates="students")
    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")
```

- `mapped_column` declares a column and its constraints (`nullable=False` means the DB
  will reject a row that has no value for this field)
- `ForeignKey("courses.id")` tells SQLAlchemy (and the DB) that `course_id` must match
  an `id` in the `courses` table
- `relationship(...)` does not create a column — it gives you a Python attribute to
  navigate between related objects (`student.course`, `student.grades`)
- `cascade="all, delete-orphan"` means: when you delete a student, SQLAlchemy
  automatically deletes all their grades too

`models/__init__.py` imports every model class so that `Base.metadata` knows about all
tables by the time `create_all()` is called.

### `app/schemas/`

Each file defines three Pydantic classes for one entity.

```python
class GradeCreate(BaseModel):   # used to validate POST bodies
    score: float
    label: str
    student_id: int

class GradeUpdate(BaseModel):   # used to validate PATCH bodies
    score: float | None = None  # every field is optional
    label: str | None = None
    student_id: int | None = None

class GradeOut(BaseModel):      # used to shape the response JSON
    id: int
    score: float
    label: str
    student_id: int
    model_config = ConfigDict(from_attributes=True)  # lets Pydantic read ORM objects
```

When FastAPI sees `data: GradeCreate` in a route signature, it automatically parses the
request body JSON, validates the types, and raises a 422 if anything is wrong — before
your code even runs.

When a route declares `response_model=GradeOut`, FastAPI automatically filters the
returned data through that schema before sending it as JSON. This prevents you from
accidentally leaking internal fields.

### `app/routes/`

One file per entity. Each file creates an `APIRouter` and registers endpoint functions on
it. Routes are intentionally thin:

```python
@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = StudentService(db).get(student_id)   # delegate to service
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
```

The route does three things and only three things:
1. Receive and parse inputs (FastAPI does this automatically via type hints)
2. Call the service
3. Return the result or raise an HTTP error

No SQL, no business rules, no data manipulation.

### `app/services/`

One file per entity. This is where the actual work happens. Each service is a class
initialized with a database session:

```python
class StudentService:
    def __init__(self, db: Session):
        self.db = db             # store the session as state

    def get(self, student_id: int) -> dict | None:
        row = self.db.execute(
            text("SELECT id, name, age, course_id FROM students WHERE id = :id"),
            {"id": student_id},
        ).fetchone()
        if row is None:
            return None
        return {"id": row.id, "name": row.name, "age": row.age, "course_id": row.course_id}
```

Note the `:id` placeholder in the SQL string. You never write `f"WHERE id = {student_id}"`.
That would be a **SQL injection vulnerability** — a user could pass a malicious value and
delete your entire database. The parameterized form (`:id` with a dict) tells SQLAlchemy
to escape the value safely.

Services return plain Python dicts (not ORM objects) because dicts are simple to test and
to serialize to JSON.

### `tests/`

One test file per entity. Tests use an in-memory SQLite database (it lives in RAM only,
reset between tests) and override the `get_db` dependency so routes use the test database
instead of `school.db`. This means tests are fast, isolated, and do not leave data behind.

---

## 8. How the server starts up

When you run `uvicorn app.main:app --reload --port 1234`, here is what happens step by step:

1. **Python imports `app/main.py`** — this triggers all other imports
2. **`from app import models`** — importing the models package runs `models/__init__.py`,
   which imports every model class. This registers all table definitions with `Base.metadata`
3. **`Base.metadata.create_all(bind=engine)`** — SQLAlchemy looks at every class that
   inherits from `Base`, compares it against what tables already exist in `school.db`,
   and creates any missing tables. If `school.db` does not exist, it is created now
4. **Routers are included** — FastAPI registers every route function under its path and method
5. **Uvicorn starts listening** on port 1234 for incoming TCP connections
6. **`--reload`** makes uvicorn watch the source files and restart when you save a change

From this point on, every incoming HTTP request is handled by a worker that runs the
matching route function.

---

## 9. What happens on a single request

Let's trace `POST /grades` with body `{"score": 18.5, "label": "Math midterm", "student_id": 1}`:

```
1. Uvicorn receives TCP bytes on port 1234
2. FastAPI parses the HTTP request — method=POST, path=/grades
3. FastAPI finds the matching route: create_grade() in routes/grades.py
4. FastAPI parses the JSON body and validates it against GradeCreate
   → if student_id is missing, it returns 422 right here, before our code runs
5. FastAPI calls get_db(), opens a SQLAlchemy session, passes it as `db`
6. create_grade() calls GradeService(db).create(data)
7. GradeService.create() runs:
   a. SELECT from students to check student_id=1 exists
   b. If not found → return None → route raises 400
   c. If found → INSERT into grades
   d. db.commit() → SQLAlchemy flushes the INSERT to school.db
   e. calls self.get(new_id) → SELECT to fetch the just-inserted row
   f. returns a dict
8. create_grade() returns the dict
9. FastAPI filters it through GradeOut and serializes to JSON
10. FastAPI sends HTTP 201 + JSON body back to the client
11. get_db()'s finally block closes the session
```

---

## 10. The database relationships

```
Teachers
  │  id, name, subject
  │
  │  one teacher teaches many courses
  │
  ├──▶ Courses
  │       │  id, name, teacher_id (FK → teachers.id)
  │       │
  │       │  one course has many students
  │       │
  │       └──▶ Students
  │                │  id, name, age, course_id (FK → courses.id)
  │                │
  │                │  one student has many grades
  │                │
  │                └──▶ Grades
  │                         id, score, label, student_id (FK → students.id)
```

A **foreign key** (FK) is a column whose value must match the primary key (`id`) of a row
in another table. If you try to insert a grade with `student_id=99` and no student with
`id=99` exists, the database will refuse the insert.

**Cascading deletes** mean: if you delete a teacher, all their courses are automatically
deleted. If you delete a course, all its students are deleted. If you delete a student,
all their grades are deleted. SQLAlchemy handles this automatically because of the
`cascade="all, delete-orphan"` on the relationship definitions.

---

## 11. Running the project

```bash
cd backend

# Create and activate a virtual environment (isolates dependencies)
python3 -m venv .venv
source .venv/bin/activate        # Mac/Linux
# .venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Start the development server
uvicorn app.main:app --reload --port 1234
```

Open http://127.0.0.1:1234/docs in your browser. FastAPI generates a full interactive UI
for every endpoint. You can try every route from this page without writing any code.

**Running tests:**

```bash
pytest
```

Tests run in-memory and do not affect `school.db`.

**Seeing the database directly:**

Download "DB Browser for SQLite" (free), open the file `backend/school.db`, and you can
browse every table and every row as if it were a spreadsheet.

---

## 12. How to read the repo and complete the exercise

### What is already done

Everything for `teachers`, `courses`, and `students` is fully implemented and working.
These are your **reference implementations** — read them before writing anything.

`grades` has been scaffolded for you:

| File | State |
|------|-------|
| `app/models/grade.py` | Complete — the table is defined |
| `app/schemas/grade.py` | Complete — Create, Update, Out are all defined |
| `app/routes/grades.py` | Skeleton — routes exist but return stubs |
| `app/services/grade_service.py` | Skeleton — all methods are empty with TODO comments |

### Suggested reading order

Before touching `grades`, read these files in this order:

1. **`app/models/student.py`** — understand how a model is defined
2. **`app/schemas/student.py`** — understand Create / Update / Out
3. **`app/services/student_service.py`** — this is your main reference. Read every method
   carefully. Notice how `create()` checks the foreign key before inserting. Notice how
   `update()` only builds a SET clause for the fields that were actually sent
4. **`app/routes/students.py`** — see how thin a route is. It calls the service, checks
   if the result is None, and raises the right error

### How to complete the exercise

Work entity by entity, method by method. Do not try to implement everything at once.

**Step 1 — implement `GradeService.list_all()`**

Open `app/services/grade_service.py`. The comment tells you what to do. Look at
`StudentService.list_all()` as a reference. The only difference is the column names
(`score`, `label`, `student_id` instead of `name`, `age`, `course_id`).

Test it: start the server, open `/docs`, call `GET /grades`. You should get `[]` (empty
list) at first — that is correct. Once implemented, it should return a list of grade objects.

**Step 2 — implement `GradeService.get()`**

Same pattern as `StudentService.get()`. Query by `id`, return `None` if nothing found.

Test it: call `GET /grades/1`. You should get a 404 (because there is nothing yet — but
the route is calling your service correctly).

**Step 3 — implement `GradeService.create()`**

This is the most important method. Steps:
1. Check that the `student_id` exists in the `students` table (look at how `StudentService`
   checks `course_id`)
2. If not found, return `None` (the route turns that into a 400)
3. INSERT into `grades`, commit, return `self.get(result.lastrowid)`

Test it: call `POST /grades` with a valid `student_id`. You should get a 201 with the
created grade. Then call it with a fake `student_id=9999` and confirm you get a 400.

**Step 4 — wire the routes**

Now open `app/routes/grades.py`. For each route, replace the stub with the real call
to the service — exactly like `routes/students.py`. Each route comment tells you:
- which service method to call
- what to return on success
- which error to raise when the service returns `None` or `False`

**Step 5 — implement `GradeService.update()` and `GradeService.delete()`**

The hardest one is `update()`. Look at `StudentService.update()` closely:
- `data.model_dump(exclude_unset=True)` only returns the fields the client actually sent
  (so a PATCH with just `{"score": 20}` does not wipe out `label` and `student_id`)
- The SET clause is built dynamically from those fields
- If `student_id` is being changed, it validates the new value

`delete()` is straightforward: check existence, delete, commit, return `True`.

**How to know you are done**

Start the server and walk through this sequence in `/docs`:

1. First create a teacher, then a course assigned to that teacher, then a student assigned
   to that course (this is required because grades depend on students)
2. `POST /grades` with a valid `student_id` → should return 201
3. `GET /grades` → should list your grade
4. `GET /grades/{id}` → should return that specific grade
5. `PATCH /grades/{id}` with `{"score": 20}` → should update only the score
6. `GET /grades/{id}` again → confirm the score changed, label did not
7. `DELETE /grades/{id}` → should return 204
8. `GET /grades/{id}` → should return 404

If all eight steps work, you have implemented the full CRUD cycle.
