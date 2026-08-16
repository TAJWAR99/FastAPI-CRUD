from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Task API",
    version="1.0.0",
    description="A simple task management API built with FastAPI.",
)


tasks: list[dict[str, Any]] = [
    {"id": 1, "title": "Task 1", "done": True},
    {"id": 2, "title": "Task 2", "done": False},
    {"id": 3, "title": "Task 3", "done": False},
]


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Task title")
    done: bool = Field(default=False, description="Completion status")


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, description="Updated task title")
    done: bool | None = Field(default=None, description="Updated completion status")


@app.get("/")
async def read_root() -> dict[str, Any]:
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "GET /",
            "GET /health",
            "GET /tasks",
            "GET /tasks/{id}",
            "POST /tasks",
            "PUT /tasks/{id}",
            "DELETE /tasks/{id}",
        ],
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks")
async def get_tasks() -> dict[str, list[dict[str, Any]]]:
    return {"tasks": tasks}


@app.get("/tasks/{task_id}")
async def get_task(task_id: int) -> dict[str, Any]:
    task = next((item for item in tasks if item["id"] == task_id), None)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return {"task": task}


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate) -> dict[str, Any]:
    new_task = {"id": len(tasks) + 1, "title": task.title, "done": task.done}
    tasks.append(new_task)
    return {"message": "Created", "task": new_task}


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: TaskUpdate) -> dict[str, Any]:
    for index, item in enumerate(tasks):
        if item["id"] == task_id:
            if task.title is not None:
                item["title"] = task.title
            if task.done is not None:
                item["done"] = task.done
            return {"message": "Updated", "task": item}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found",
    )


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int) -> Response:
    for index, item in enumerate(tasks):
        if item["id"] == task_id:
            tasks.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
