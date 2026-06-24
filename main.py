from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "Post 1"}

@app.post("/posts")
def create_post(new_post: Post):
    print(new_post)
    return {"newpost": f"title: {new_post.title}  -  content: {new_post.content}"}
