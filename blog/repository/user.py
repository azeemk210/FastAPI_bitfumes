from sqlalchemy.orm import Session
from blog import models, schemas
from fastapi import HTTPException, status
from blog.hashing import Hash

def create_user(request: schemas.User, db: Session):
    hashed_password = Hash.get_password(request.password)
    user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def get_all_users(db: Session):
    return db.query(models.User).all()

def delete_user(user_id: int, db: Session):
    user = get_user(user_id, db)
    db.delete(user)
    db.commit()