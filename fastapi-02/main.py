from fastapi import FastAPI

app = FastAPI()

@app.get("/") # GET /
def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}") # GET /items/{item_id}
def read_item(item_id: int):
    return {"item_id": item_id}