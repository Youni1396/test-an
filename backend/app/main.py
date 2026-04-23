"""
Application entry point.

This is where all the pieces come together:
- create the FastAPI app
- create the DB tables on startup (for a teaching app; in production you'd
  use a migration tool like Alembic instead)
- include the routers from routes/ so their endpoints are live

Run locally with:
    uvicorn app.main:app --reload --port 1234
Then open http://127.0.0.1:1234/docs for the auto-generated API UI.
"""

from fastapi import FastAPI

from app.database import Base, engine
# Importing the models package registers every model class with Base.metadata
# so create_all() knows which tables to create.
from app import models  # noqa: F401
from app.routes import teachers, courses, students


def create_app() -> FastAPI:
    app = FastAPI(
        title="School API",
        description="A tiny teaching backend: teachers, courses, and students.",
        version="0.1.0",
    )

    # Create the SQLite tables if they don't exist yet.
    Base.metadata.create_all(bind=engine)

    # Register each entity's routes under the app.
    app.include_router(teachers.router)
    app.include_router(courses.router)
    app.include_router(students.router)

    @app.get("/", tags=["root"])
    def root():
        return {"message": "School API is running. See /docs."}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=1234, reload=True)
