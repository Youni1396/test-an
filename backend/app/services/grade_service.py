from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.grade import GradeCreate, GradeUpdate


class GradeService:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[dict]:
        # TODO: query all rows from the `grades` table
        # Hint: look at how StudentService.list_all() does it with text()
        # Return a list of dicts with keys: id, score, label, student_id
        return []

    def get(self, grade_id: int) -> dict | None:
        # TODO: query a single grade by its id
        # Hint: use a WHERE id = :id clause, same pattern as StudentService.get()
        # Return None if the row doesn't exist
        return None

    def create(self, data: GradeCreate) -> dict | None:
        # TODO: before inserting, check that the student_id actually exists in the `students` table
        # If the student doesn't exist, return None (the route will turn that into a 400)
        # Then INSERT into `grades` and return the newly created grade via self.get()
        # Don't forget to commit!
        return None

    def update(self, grade_id: int, data: GradeUpdate) -> dict | None:
        # TODO: check the grade exists first (return None → 404 if not)
        # Build a dynamic SET clause from data.model_dump(exclude_unset=True)
        # If student_id is being changed, verify the new student exists
        # Execute the UPDATE, commit, and return the updated grade via self.get()
        return None

    def delete(self, grade_id: int) -> bool:
        # TODO: check the grade exists first (return False → 404 if not)
        # Execute DELETE FROM grades WHERE id = :id, commit, and return True
        return False
