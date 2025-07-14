from fastapi import APIRouter, Depends, status, Response
from blog import schemas
from blog.database import get_db
from sqlalchemy.orm import Session
from blog.repository import user

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create_user(request, db)

@router.get("/", response_model=list[schemas.ShowUser])
def get_users(db: Session = Depends(get_db)):
    return user.get_all_users(db)

@router.get("/{user_id}", response_model=schemas.ShowUserWithBlogs)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user.get_user(user_id, db)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user.delete_user(user_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)