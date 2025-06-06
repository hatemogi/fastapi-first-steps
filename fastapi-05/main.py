from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

app = FastAPI()

@app.get("/") # GET /
def root():
    return {"message": "Hello World"}

class ItemColor(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"

class ItemBase(BaseModel):
    name: str = Field(description="상품명")
    color: Optional[ItemColor] = Field(default=None, description="상품 색상")

class Item(ItemBase):
    id: int

temp_items = {
    1: Item(id=1, name="아이템A", color=ItemColor.red),
    2: Item(id=2, name="아이템B", color=ItemColor.green),
}

def item_or_404(item_id: int) -> Item:
    if item_id not in temp_items:
        raise HTTPException(status_code=404, detail="아이템이 없어요")
    return temp_items[item_id]
    
@app.get("/items/{item_id}") # GET /items/{item_id}
def read_item(item_id: int) -> Item:
    return item_or_404(item_id)

@app.post("/items", status_code=201, summary="2.1 상품등록 0516") # POST /items
def create_item(item: Item):
    if item.id in temp_items:
        raise HTTPException(status_code=400, detail="아이템이 이미 있어요")
    temp_items[item.id] = item
    return item

@app.put("/items/{item_id}", status_code=202)
def update_item(item_id: int, new_item: ItemBase):
    item = item_or_404(item_id)
    item.name = new_item.name
    item.color = new_item.color
    return {"updated": True}

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    _ = item_or_404(item_id)
    del temp_items[item_id]
    return {"deleted": True}

