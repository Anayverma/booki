from sqlalchemy.orm import Session
from ... import models, security
from . import schemas

def get_user_by_email(db: Session, email: str):
    # Fetch user by email
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # Create new user with hashed password
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user