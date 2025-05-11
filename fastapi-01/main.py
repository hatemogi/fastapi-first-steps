from fastapi import FastAPI

app = FastAPI()

@app.get("/") # GET /
def root():
    return {"message": "Hello World"}
