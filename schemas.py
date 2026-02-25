from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):

    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
        schema_extra = {"example": {"id": 1, "name": "Alice", "email": "alice@example.com"}}


class ClassCreate(BaseModel):
    
    name: str
    dateTime: str
    instructor: str
    availableSlots: int

    class Config:
        schema_extra = {
            "example": {
                "name": "Yoga Flow",
                "dateTime": "2025-06-15T10:00:00Z",
                "instructor": "John Doe",
                "availableSlots": 20,
            }
        }


class ClassOut(BaseModel):
    id: int
    name: str
    dateTime: datetime
    instructor: str
    availableSlots: int

    class Config:
        orm_mode = True
        schema_extra = {"example": {"id": 1, "name": "HIIT Session", "dateTime": "2025-06-18T08:00:00Z", "instructor": "Jane Smith", "availableSlots": 10}}


class BookingCreate(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

    class Config:
        schema_extra = {"example": {"class_id": 1, "client_name": "Alice", "client_email": "alice@example.com"}}


class BookingOut(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr
    booked_at: datetime


    class Config:
        orm_mode = True
        schema_extra = {"example": {"id": 1, "class_id": 1, "client_name": "Alice", "client_email": "alice@example.com", "booked_at": "2025-06-14T15:30:00+05:30"}}
