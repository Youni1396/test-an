from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.teacher import TeacherCreate, TeacherUpdate


class TeacherService:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[dict]:
        rows = self.db.execute(text("SELECT id, name, subject FROM teachers")).fetchall()
        print(rows)
        return [{"id": r.id, "name": r.name, "subject": r.subject} for r in rows]

    def get(self, teacher_id: int) -> dict | None:
        row = self.db.execute(
            text("SELECT id, name, subject FROM teachers WHERE id = :id"),
            {"id": teacher_id},
        ).fetchone()
        if row is None:
            return None
        return {"id": row.id, "name": row.name, "subject": row.subject}

    def create(self, data: TeacherCreate) -> dict:
        print("THE DATA IS", data)
        result = self.db.execute(
            text("INSERT INTO teachers (name, subject) VALUES (:name, :subject)"),
            {"name": data.name, "subject": data.subject},
        )
        self.db.commit()
        new_id = result.lastrowid
        return self.get(new_id)

    def update(self, teacher_id: int, data: TeacherUpdate) -> dict | None:
        if self.get(teacher_id) is None:
            return None
        fields = data.model_dump(exclude_unset=True)
        if not fields:
            return self.get(teacher_id)
        set_clause = ", ".join(f"{col} = :{col}" for col in fields)
        fields["id"] = teacher_id
        self.db.execute(
            text(f"UPDATE teachers SET {set_clause} WHERE id = :id"),
            fields,
        )
        self.db.commit()
        return self.get(teacher_id)

    def delete(self, teacher_id: int) -> bool:
        if self.get(teacher_id) is None:
            return False
        self.db.execute(
            text("DELETE FROM teachers WHERE id = :id"),
            {"id": teacher_id},
        )
        self.db.commit()
        return True
