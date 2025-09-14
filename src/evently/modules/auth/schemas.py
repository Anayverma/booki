from pydantic import BaseModel, EmailStr

# Base schema for user
class UserBase(BaseModel):
    email: EmailStr

# Schema for user registration
class UserCreate(UserBase):
    password: str

# Schema returned for user info
class User(UserBase):
    id: int
    role: str
    class Config:
        from_attributes = True  # Allow ORM objects

# JWT token schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Token payload schema
class TokenData(BaseModel):
    email: str | None = None