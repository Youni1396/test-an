"""
Teacher ORM model — a Python class that maps to the `teachers` table.

OOP in practice: each row in the DB becomes an instance of this class.
SQLAlchemy reads the class attributes (Column, relationship) to figure out
what the table looks like and how it connects to other tables.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    subject: Mapped[str] = mapped_column(String, nullable=False)

    # One teacher -> many courses. `back_populates` wires the two sides together.
    courses: Mapped[list["Course"]] = relationship(
        "Course", back_populates="teacher", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Teacher id={self.id} name={self.name!r}>"
