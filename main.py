from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "server"}

# http://127.0.0.1:8000/greet/tajwar
# @app.get("/greet/{name}")
# async def greet_user(name: str):
#     return {"message": f"Hello, {name}!"}

# http://127.0.0.1:8000/greet?name=tajwar --> query parameter
@app.get("/greet")
async def greet_user(name: str):
    return {"message": f"Hello, {name}!"}