"""
Student ORM model — belongs to one Course.

The `course_id` foreign key is how the DB enforces the relationship:
you can't create a student pointing to a course that doesn't exist.
"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)

    course: Mapped["Course"] = relationship("Course", back_populates="students")

    def __repr__(self) -> str:
        return f"<Student id={self.id} name={self.name!r}>"
