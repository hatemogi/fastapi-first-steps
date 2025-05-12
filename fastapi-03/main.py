from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import Enum

app = FastAPI()

class ItemColor(str, Enum):
    RED = "빨강"
    GREEN = "초록"
    BLUE= "파랑"

class ItemBase(BaseModel):
    name: str = Field(description="아이템명")
    color: ItemColor = Field(ItemColor.RED, description="색상")
    price: int = Field(10000, description="가격")

class Item(ItemBase):
    id: int = Field(description="아이템ID")

temp_items = {
    1: Item(id = 1, name = "아이템A", color = ItemColor.RED, price = 20000)
}

@app.get("/")
def root():
    return {"message": "Hello, World"}

@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    if item_id in temp_items:
        return temp_items[item_id]
    else:
        raise HTTPException(404, "Item not found")

@app.post("/items", status_code=201)
def create_item(item: ItemBase):
    return {"created": True}
