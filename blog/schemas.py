from typing import Optional, List
from pydantic import BaseModel

class BlogBase(BaseModel):
    title: str
    body: str

class ShowBlog(BlogBase):
    pass

class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    id: int
    name: str
    email: str