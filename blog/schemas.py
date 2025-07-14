from typing import Optional, List
from pydantic import BaseModel

class BlogBase(BaseModel):
    title: str
    body: str


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True

class ShowBlog(BlogBase):
    creator: ShowUser

    class Config():
        orm_mode = True


class ShowUserWithBlogs(ShowUser):
    blogs: List[BlogBase] = []

    class Config():
        orm_mode = True