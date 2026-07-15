from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
from psycopg.rows import dict_row
import psycopg
import os

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

db_name = os.getenv("DB_NAME")
db_pass = os.getenv("DB_PASS")
conn = psycopg.connect(f"host=localhost port=5432 dbname={db_name} user=postgres password={db_pass}")


posts = [
    {"title": "Busco jale", "content": "Quiero chambaaaa", "id": 0},
    {"title": "Y si si?", "content": "Podemos lograrlo, hay que confiar", "id": 1},
]
def find_post(id):
    for post in posts:
        if post.get("id") == id:
            return post
    return None
def find_index(id):
    for index, post in enumerate(posts):
        if post.get("id") == id:
            return index
    return None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""SELECT * FROM posts""")
        posts = cur.fetchall()
        return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO posts (title, content, published)
                    VALUES (%s, %s, %s) RETURNING *""", 
                    (new_post.title, new_post.content, new_post.published))
        
        post_result = cur.fetchone()
        conn.commit()
        return {"data": post_result}

@app.get("/posts/{id}")
def get_post(id: int):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""SELECT * FROM posts
                    WHERE id = %s""",
                    (id,))
        post = cur.fetchone()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {id} was not found"
            )
        
        return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM posts
                    WHERE id = %s RETURNING *""",
                    (id,))
        deleted_post = cur.fetchone()
        if not deleted_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {id} not exist."
            )
        conn.commit()
        return

@app.put("/posts/{id}")
def update_post(id: int, new_content: Post):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""UPDATE posts
                    SET title = %s, content = %s, published = %s 
                    WHERE id = %s RETURNING *""",
                    (new_content.title, new_content.content, new_content.published, id))
        post_updated = cur.fetchone()
        if not post_updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {id} desn't exist"
            )

        conn.commit()
        return {"data": post_updated}
