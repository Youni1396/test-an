from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.student import StudentCreate, StudentOut, StudentUpdate
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_db)):
    return StudentService(db).list_all()


@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = StudentService(db).get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    student = StudentService(db).create(data)
    if student is None:
        raise HTTPException(status_code=400, detail="Course does not exist")
    return student


@router.patch("/{student_id}", response_model=StudentOut)
def update_student(student_id: int, data: StudentUpdate, db: Session = Depends(get_db)):
    student = StudentService(db).update(student_id, data)
    if student is None:
        raise HTTPException(status_code=404, detail="Student or course not found")
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if not StudentService(db).delete(student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return None
