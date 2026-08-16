from fastapi import FastAPI

app = FastAPI()

# http://127.0.0.1:8000/greet/tajwar
# @app.get("/greet/{name}")
# async def greet_user(name: str):
#     return {"message": f"Hello, {name}!"}

# http://127.0.0.1:8000/greet?name=tajwar --> query parameter
# @app.get("/greet")
# async def greet_user(name: str):
#     return {"message": f"Hello, {name}!"}

@app.get("/")
async def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
async def health_check():
    return {"status": "ok"}