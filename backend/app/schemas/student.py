from pydantic import BaseModel, ConfigDict


class StudentCreate(BaseModel):
    name: str
    age: int
    course_id: int


class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    course_id: int | None = None


class StudentOut(BaseModel):
    id: int
    name: str
    age: int
    course_id: int

    model_config = ConfigDict(from_attributes=True)
