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
tasks = [
    {"id": 1, "title": "Task 1", "done": True},
    {"id": 2, "title": "Task 2", "done": True},
    {"id": 3, "title": "Task 3", "done": False},
]

@app.get("/")
async def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/tasks")
async def get_tasks():
    return {"tasks": tasks}

@app.get("/tasks/{id}")
async def get_task(id: int):
    try:
        return {"task": tasks[id-1]}
    except IndexError:
        return {"error": f"Task {id} not found"}, 404