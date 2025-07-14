from fastapi import APIRouter
from .. import schemas, models
from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from blog.database import engine, get_db
from sqlalchemy.orm  import Session


router = APIRouter(
    prefix = "/blog",
     tags=['Blogs']

)


@router.post("/", status_code=201)
def create_blog(request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

@router.get("/", status_code=200, response_model=List[schemas.BlogBase])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get("/{blog_id}", status_code=200, response_model=schemas.ShowBlog)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with ID {blog_id} not found"
        )
    return blog


@router.delete("/{blog_id}", status_code=204)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with ID {blog_id} not found"
        )
    db.delete(blog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{blog_id}", status_code=200)
def update_blog(blog_id: int, request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with ID {blog_id} not found"
        )
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog


