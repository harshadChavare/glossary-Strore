import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Initialize the FastAPI app
app = FastAPI()

# Define the ToDo model
class ToDo(BaseModel):
    task: str
    done: bool = False

# Initialize an empty list to store to-dos
todos = []

# Function to get all ToDos
def get_todos():
    return todos

# Function to create a new ToDo
def create_todo(todo: ToDo):
    todos.append(todo)
    return todo

# Function to update an existing ToDo
def update_todo(todo_id: int, todo: ToDo):
    if todo_id >= len(todos):
        raise HTTPException(status_code=404, detail="ToDo not found")
    todos[todo_id] = todo
    return todo

# Function to delete a ToDo
def delete_todo(todo_id: int):
    if todo_id >= len(todos):
        raise HTTPException(status_code=404, detail="ToDo not found")
    deleted_todo = todos.pop(todo_id)
    return {"message": f"ToDo '{deleted_todo.task}' deleted successfully!"}

# Define the routes using function-based views
@app.get("/todos", response_model=List[ToDo])
def read_todos():
    return get_todos()

@app.post("/todos", response_model=ToDo)
def add_todo(todo: ToDo):
    return create_todo(todo)

@app.put("/todos/{todo_id}", response_model=ToDo)
def modify_todo(todo_id: int, todo: ToDo):
    return update_todo(todo_id, todo)

@app.delete("/todos/{todo_id}")
def remove_todo(todo_id: int):
    return delete_todo(todo_id)


# Run the app using uvicorn
if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)
