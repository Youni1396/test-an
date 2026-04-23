from pydantic import BaseModel, ConfigDict


class GradeCreate(BaseModel):
    score: float
    label: str
    student_id: int


class GradeUpdate(BaseModel):
    score: float | None = None
    label: str | None = None
    student_id: int | None = None


class GradeOut(BaseModel):
    id: int
    score: float
    label: str
    student_id: int

    model_config = ConfigDict(from_attributes=True)
