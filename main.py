from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

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
        return {"task": [task for task in tasks if task["id"] == id][0]}
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task {id} not found"
        )

class taskModel(BaseModel):
    title: str
    done: bool = False

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(task: taskModel):
    if task.title == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Task title cannot be empty"
        )
    new_task = {"id": len(tasks) + 1, "title": task.title, "done": False}
    tasks.append(new_task)
    return {"message" : "Created"}

@app.put("/tasks/{id}")
async def update_task(id: int, task: taskModel):
    for item in tasks:
        if item["id"] == id:
            if task.title == "":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Invalid body"
                )
            if item["title"] != "":
                item["title"] = task.title
            if item["done"] != "":
                item["done"] = task.done
            return {"message": "done", "tasks": tasks}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task {id} not found"
    )

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int):
    for item in tasks:
        if item["id"] == id:
            tasks.remove(item)
            return {"message": "No Content"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task {id} not found"
    )