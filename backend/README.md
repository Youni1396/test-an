# School API — a tiny teaching backend

This project is designed to answer one question:
**what is a backend, and how does it work together with a database to serve a frontend?**

There's no frontend here on purpose — we want to focus on the server side.
Instead, you'll use the auto-generated Swagger UI (at `/docs`) to poke the API
like a frontend would.

## The big picture

```
┌──────────┐   HTTP   ┌──────────────────────────────┐   SQL   ┌───────────┐
│ Frontend │ ───────▶ │          Backend             │ ──────▶ │ Database  │
│ (browser)│ ◀─────── │ (this FastAPI app)           │ ◀────── │ (SQLite)  │
└──────────┘   JSON   └──────────────────────────────┘   rows  └───────────┘
```

- The **frontend** speaks HTTP + JSON.
- The **backend** translates that into **SQL** queries the database understands.
- The **database** stores data on disk and answers queries.

Our job in this project is the middle box.

## How the code is organized

```
backend/
├── app/
│   ├── main.py          ← FastAPI app, wires everything together
│   ├── database.py      ← DB connection + session factory
│   ├── models/          ← SQLAlchemy classes — "what a row LOOKS LIKE in the DB"
│   ├── schemas/         ← Pydantic classes — "what JSON the API accepts/returns"
│   ├── routes/          ← HTTP endpoints — thin, just parse & return
│   └── services/        ← Business logic — rules, orchestration, DB calls
├── tests/               ← One test file per entity
├── diagram.md           ← Database diagram
└── requirements.txt
```

### Why four layers?

Each layer has **one job**. If you open a file, you know what kind of code to expect.

| Layer     | Answers the question              | Example                                 |
|-----------|-----------------------------------|-----------------------------------------|
| routes    | *How does HTTP map to my code?*   | `POST /students` → call a service       |
| services  | *What are the business rules?*    | "can't add a student to a missing course" |
| models    | *What does the DB look like?*     | `students` table has `id, name, age, course_id` |
| schemas   | *What JSON do we exchange?*       | `{"name": "Alex", "age": 15, ...}`      |

Without this split, every route file would be a 300-line monster mixing HTTP,
business logic, and SQL. With it, each file stays small and focused.

## OOP in this project

Your friend wanted to learn classes — here's where they show up:

- **`models/*.py`** — each model (`Teacher`, `Course`, `Student`) is a class
  inheriting from `Base`. SQLAlchemy reads the class to figure out the table.
- **`services/*.py`** — each service is a class that holds the DB session as
  state (`self.db`) and exposes methods like `create`, `update`, `delete`.
  This is classic OOP: **bundle data with the functions that act on it**.
- **`schemas/*.py`** — each schema is a Pydantic class. Pydantic validates JSON
  against the class's type hints automatically.

## Getting started

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs — FastAPI generates a clickable UI for
every endpoint. This is how you "talk to the backend" without a frontend.

## Running the tests

```bash
pytest
```

Tests use an in-memory SQLite so they're fast and don't touch `school.db`.

## The endpoints

Every entity has the same 5 operations (this pattern is called **CRUD**):

| Method | Path                      | What it does                     |
|--------|---------------------------|----------------------------------|
| GET    | `/{entity}`               | List all                         |
| GET    | `/{entity}/{id}`          | Get one by ID                    |
| POST   | `/{entity}`               | Create                           |
| PATCH  | `/{entity}/{id}`          | Update (partial)                 |
| DELETE | `/{entity}/{id}`          | Delete                           |

where `{entity}` is `teachers`, `courses`, or `students`.

## What to try first

1. Start the server.
2. Open `/docs`.
3. `POST /teachers` with `{"name": "Ms. Ada", "subject": "Math"}`.
4. `POST /courses` with `{"name": "Algebra", "teacher_id": 1}`.
5. `POST /students` with `{"name": "Alex", "age": 15, "course_id": 1}`.
6. `GET /students` — see what you created.
7. Try `POST /courses` with a `teacher_id` that doesn't exist — watch the 400.

That last step is the key lesson: **the backend enforces rules the frontend can't
be trusted to enforce on its own.** That's why backends exist.

See [diagram.md](diagram.md) for the database relationships.
