from fastapi import FastAPI
from blog import models, schemas
from blog.database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.post("/blogs/")
def create_blog(request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = models.Blog(**request.dict())
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog
