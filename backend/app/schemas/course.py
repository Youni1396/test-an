from pydantic import BaseModel, ConfigDict


class CourseCreate(BaseModel):
    name: str
    teacher_id: int


class CourseUpdate(BaseModel):
    name: str | None = None
    teacher_id: int | None = None


class CourseOut(BaseModel):
    id: int
    name: str
    teacher_id: int

    model_config = ConfigDict(from_attributes=True)
