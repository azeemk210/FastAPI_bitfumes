from fastapi import APIRouter, Depends, status, Response
from blog import schemas
from blog.database import get_db
from sqlalchemy.orm import Session
from blog.repository import blog

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)

@router.get("/", response_model=list[schemas.ShowBlog])
def get_blogs(db: Session = Depends(get_db)):
    return blog.get_all_blogs(db)

@router.get("/{blog_id}", response_model=schemas.ShowBlog)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    return blog.get_blog(blog_id, db)

@router.post("/", response_model=schemas.ShowBlog, status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.BlogBase, db: Session = Depends(get_db), user_id: int = 1):
    return blog.create_blog(request, db, user_id)

@router.put("/{blog_id}", response_model=schemas.ShowBlog)
def update_blog(blog_id: int, request: schemas.BlogBase, db: Session = Depends(get_db)):
    return blog.update_blog(blog_id, request, db)

@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog.delete_blog(blog_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)