"""
HTTP layer for teachers.

Routes stay THIN on purpose:
1. Parse the request (FastAPI does this via the schema type hints).
2. Call the service.
3. Translate the result to HTTP (200/404/etc.).

No DB queries here, no business rules — those belong in the service.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.teacher import TeacherCreate, TeacherOut, TeacherUpdate
from app.services.teacher_service import TeacherService

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get("", response_model=list[TeacherOut])
def list_teachers(db: Session = Depends(get_db)):
    return TeacherService(db).list_all()


@router.get("/{teacher_id}", response_model=TeacherOut)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = TeacherService(db).get(teacher_id)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@router.post("", response_model=TeacherOut, status_code=status.HTTP_201_CREATED)
def create_teacher(data: TeacherCreate, db: Session = Depends(get_db)):
    return TeacherService(db).create(data)


@router.patch("/{teacher_id}", response_model=TeacherOut)
def update_teacher(teacher_id: int, data: TeacherUpdate, db: Session = Depends(get_db)):
    teacher = TeacherService(db).update(teacher_id, data)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    if not TeacherService(db).delete(teacher_id):
        raise HTTPException(status_code=404, detail="Teacher not found")
    return None
