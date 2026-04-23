from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.course import CourseCreate, CourseUpdate


class CourseService:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[dict]:
        rows = self.db.execute(text("SELECT id, name, teacher_id FROM courses")).fetchall()
        return [{"id": r.id, "name": r.name, "teacher_id": r.teacher_id} for r in rows]

    def get(self, course_id: int) -> dict | None:
        row = self.db.execute(
            text("SELECT id, name, teacher_id FROM courses WHERE id = :id"),
            {"id": course_id},
        ).fetchone()
        if row is None:
            return None
        return {"id": row.id, "name": row.name, "teacher_id": row.teacher_id}

    def create(self, data: CourseCreate) -> dict | None:
        teacher = self.db.execute(
            text("SELECT id FROM teachers WHERE id = :id"),
            {"id": data.teacher_id},
        ).fetchone()
        if teacher is None:
            return None
        result = self.db.execute(
            text("INSERT INTO courses (name, teacher_id) VALUES (:name, :teacher_id)"),
            {"name": data.name, "teacher_id": data.teacher_id},
        )
        self.db.commit()
        return self.get(result.lastrowid)

    def update(self, course_id: int, data: CourseUpdate) -> dict | None:
        if self.get(course_id) is None:
            return None
        fields = data.model_dump(exclude_unset=True)
        if not fields:
            return self.get(course_id)
        if "teacher_id" in fields:
            teacher = self.db.execute(
                text("SELECT id FROM teachers WHERE id = :id"),
                {"id": fields["teacher_id"]},
            ).fetchone()
            if teacher is None:
                return None
        set_clause = ", ".join(f"{col} = :{col}" for col in fields)
        fields["id"] = course_id
        self.db.execute(
            text(f"UPDATE courses SET {set_clause} WHERE id = :id"),
            fields,
        )
        self.db.commit()
        return self.get(course_id)

    def delete(self, course_id: int) -> bool:
        if self.get(course_id) is None:
            return False
        self.db.execute(
            text("DELETE FROM courses WHERE id = :id"),
            {"id": course_id},
        )
        self.db.commit()
        return True
