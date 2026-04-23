from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.student import StudentCreate, StudentUpdate


class StudentService:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[dict]:
        rows = self.db.execute(text("SELECT id, name, age, course_id FROM students")).fetchall()
        return [{"id": r.id, "name": r.name, "age": r.age, "course_id": r.course_id} for r in rows]

    def get(self, student_id: int) -> dict | None:
        row = self.db.execute(
            text("SELECT id, name, age, course_id FROM students WHERE id = :id"),
            {"id": student_id},
        ).fetchone()
        if row is None:
            return None
        return {"id": row.id, "name": row.name, "age": row.age, "course_id": row.course_id}

    def create(self, data: StudentCreate) -> dict | None:
        course = self.db.execute(
            text("SELECT id FROM courses WHERE id = :id"),
            {"id": data.course_id},
        ).fetchone()
        if course is None:
            return None
        result = self.db.execute(
            text("INSERT INTO students (name, age, course_id) VALUES (:name, :age, :course_id)"),
            {"name": data.name, "age": data.age, "course_id": data.course_id},
        )
        self.db.commit()
        return self.get(result.lastrowid)

    def update(self, student_id: int, data: StudentUpdate) -> dict | None:
        if self.get(student_id) is None:
            return None
        fields = data.model_dump(exclude_unset=True)
        if not fields:
            return self.get(student_id)
        if "course_id" in fields:
            course = self.db.execute(
                text("SELECT id FROM courses WHERE id = :id"),
                {"id": fields["course_id"]},
            ).fetchone()
            if course is None:
                return None
        set_clause = ", ".join(f"{col} = :{col}" for col in fields)
        fields["id"] = student_id
        self.db.execute(
            text(f"UPDATE students SET {set_clause} WHERE id = :id"),
            fields,
        )
        self.db.commit()
        return self.get(student_id)

    def delete(self, student_id: int) -> bool:
        if self.get(student_id) is None:
            return False
        self.db.execute(
            text("DELETE FROM students WHERE id = :id"),
            {"id": student_id},
        )
        self.db.commit()
        return True
