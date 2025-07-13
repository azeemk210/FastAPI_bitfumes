from fastapi import FastAPI, Depends, status, Response, HTTPException
from blog import models, schemas
from blog.database import engine, get_db
from sqlalchemy.orm  import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.post("/blogs/", status_code=201)
def create_blog(request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = models.Blog(title=request.title, body=request.body)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

@app.get("/blogs/", status_code=200)
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blogs/{blog_id}", status_code=200)
def get_blog(blog_id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with ID {blog_id} not found"
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with ID {blog_id} not found"}
    return blog