from sqlalchemy.orm import Session
from blog import models, schemas
from fastapi import HTTPException, status

def get_blog(blog_id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

def get_all_blogs(db: Session):
    return db.query(models.Blog).all()

def create_blog(request: schemas.BlogBase, db: Session, user_id: int):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def update_blog(blog_id: int, request: schemas.BlogBase, db: Session):
    blog = get_blog(blog_id, db)
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog

def delete_blog(blog_id: int, db: Session):
    blog = get_blog(blog_id, db)
    db.delete(blog)
    db.commit()