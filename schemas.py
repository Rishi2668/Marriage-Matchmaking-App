from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class UserBase(BaseModel):
    name: str
    age: int
    gender: str = Field(..., pattern="(?i)^(male|female)$", min_length=3)
    email: EmailStr
    city: str
    interests: List[str]

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = Field(None, pattern="^(male|female)$", min_length=3)
    email: Optional[EmailStr] = None
    city: Optional[str] = None
    interests: Optional[List[str]] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True  

        # 