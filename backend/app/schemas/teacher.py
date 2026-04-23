"""
Pydantic schemas describe the JSON shapes the API accepts and returns.

Why separate from ORM models?
- Models = what the DB stores.
- Schemas = what the API exposes.
These are two different concerns: e.g. the DB has an internal `id` the client
doesn't set on create, or you might hide fields from responses.
"""

from pydantic import BaseModel, ConfigDict


class TeacherCreate(BaseModel):
    """Shape of the JSON the client sends to create a teacher."""
    name: str
    subject: str


class TeacherUpdate(BaseModel):
    """All fields optional — client can update just what they want."""
    name: str | None = None
    subject: str | None = None


class TeacherOut(BaseModel):
    """Shape of the JSON the API sends back."""
    id: int
    name: str
    subject: str

    # Lets Pydantic read attributes off a SQLAlchemy object directly.
    model_config = ConfigDict(from_attributes=True)
