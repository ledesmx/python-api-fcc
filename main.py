from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "Post 1"}

@app.post("/createpost")
def create_post():
    return {"message": "Post created successfully"}