from typing import List
from fastapi import APIRouter
from fastapi import FastAPI, Depends, status, Response, HTTPException
from blog import models, schemas
from blog.database import engine, get_db
from sqlalchemy.orm  import Session
from blog.hashing import Hash

router = APIRouter(
    prefix = "/user",
    tags=['Users'] 
)

@router.post("/", response_model= schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
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

@router.get("/", status_code=200, response_model=List[schemas.ShowUser])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/{user_id}", status_code=200, response_model=schemas.ShowUserWithBlogs)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)