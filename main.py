from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

posts = [
    {"title": "Busco jale", "content": "Quiero chambaaaa", "id": 0},
    {"title": "Y si si?", "content": "Podemos lograrlo, hay que confiar", "id": 1},
]
def find_post(id):
    for post in posts:
        if post.get("id") == id:
            return post
    return None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    # Fastapi serializes it automatically
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    post_dict = new_post.model_dump()
    # Usually tha DB do this, but for now I'm going to hardcode it
    post_dict["id"] = randrange(0,1000)
    posts.append(post_dict)
    print(new_post)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )
    return {"data": post}
