from datetime import datetime
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import declarative_base
from database import db_instance

Base = declarative_base(metadata=db_instance.metadata)


class User(Base):
    __table__ = db_instance.metadata.tables["users"]


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str

    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("date_of_birth must be in 'YYYY-MM-DD' format")
        return v


class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: str

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            first_name=obj.first_name,
            last_name=obj.last_name,
            date_of_birth=obj.date_of_birth.strftime("%Y-%m-%d"),
        )

    class Config:
        orm_mode = True
