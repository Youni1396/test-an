"""
Grade ORM model — belongs to one Student.

A grade records the score a student received, tied to a specific student.
The `student_id` foreign key enforces the relationship at the DB level:
you can't create a grade for a student that doesn't exist.
"""

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    # e.g. "Math midterm", "History final" — a label for the graded item
    label: Mapped[str] = mapped_column(String, nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)

    student: Mapped["Student"] = relationship("Student", back_populates="grades")

    def __repr__(self) -> str:
        return f"<Grade id={self.id} student_id={self.student_id} score={self.score}>"
