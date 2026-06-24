from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "Post 1"}

@app.post("/createpost")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"newpost": f"title: {payload.get("title")}  -  content: {payload.get("content")}"}
