from typing import Any, List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class CourseCreate(BaseModel):
    name: str
    file: bytes  # Accepts a blob
    user_id: int

# Output schema
class CourseCreateResponse(BaseModel):
    id: int
    name: str
    pdf_files: str # URL or path stored as a string, default is NULL
    user_id: int
    conversation: Optional[dict] = None  # JSON data, default is NULL
    created_at: datetime
    