from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from blog import models, schemas
from blog.database import engine, get_db
from sqlalchemy.orm  import Session
from blog.hashing import Hash


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/blogs/", status_code=201, tags=['blogs'])
def create_blog(request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = models.Blog(title=request.title, body=request.body)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

@app.get("/blogs/", status_code=200, response_model=List[schemas.ShowBlog], tags=['blogs'])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blogs/{blog_id}", status_code=200, response_model=schemas.ShowBlog, tags=['blogs'])
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with ID {blog_id} not found"
        )
    return blog


@app.delete("/blogs/{blog_id}", status_code=204, tags=['blogs'])
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

@app.put("/blogs/{blog_id}", status_code=200, tags=['blogs'])
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




@app.post("/user", response_model= schemas.ShowUser, tags=['users'] )
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

@app.get("/users/", status_code=200, response_model=List[schemas.ShowUser], tags=['users'])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/users/{user_id}", status_code=200, response_model=schemas.ShowUser, tags=['users'])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.qeury(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@app.delete("/users/{user_id}", status_code=204, tags=['users'])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with ID {user_id} not found"
        )
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)