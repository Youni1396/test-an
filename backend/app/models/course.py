"""
Course ORM model — belongs to one Teacher, has many Students.

This is the "middle" entity and shows both sides of a relationship:
- a foreign key pointing UP to teachers
- a relationship pointing DOWN to students
"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)

    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="courses")
    students: Mapped[list["Student"]] = relationship(
        "Student", back_populates="course", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Course id={self.id} name={self.name!r}>"
