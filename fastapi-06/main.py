from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
import nanoid
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, select, insert, update, delete
from sqlalchemy.exc import NoResultFound

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/dbname")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Reflect existing table schema from database
items_table = Table('items', metadata, autoload_with=engine)

@app.get("/") # GET /
def root():
    return {"message": "Hello World"}

type ItemId = str

class ItemColor(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"

class ItemBase(BaseModel):
    name: str = Field(description="상품명")
    color: Optional[ItemColor] = Field(default=None, description="상품 색상")

class Item(ItemBase):
    id: ItemId

def item_or_404(item_id: ItemId) -> Item:
    with engine.connect() as conn:
        result = conn.execute(select(items_table).where(items_table.c.id == item_id)).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="아이템이 없어요")
        return Item(id=result.id, name=result.name, color=result.color)

@app.get("/items/{item_id}") # GET /items/{item_id}
def read_item(item_id: ItemId) -> Item:
    return item_or_404(item_id)

@app.post("/items", status_code=201, summary="2.1 상품등록 0516") # POST /items
def create_item(item: ItemBase):
    id: ItemId = nanoid.generate(size=10)
    with engine.connect() as conn:
        # Check if ID already exists
        existing = conn.execute(select(items_table).where(items_table.c.id == id)).fetchone()
        if existing:
            raise HTTPException(status_code=407, detail="아이템이 이미 있어요")

        # Insert new item
        conn.execute(insert(items_table).values(
            id=id,
            name=item.name,
            color=item.color
        ))
        conn.commit()

        return Item(**item.model_dump(), id=id)

@app.put("/items/{item_id}", status_code=202)
def update_item(item_id: ItemId, new_item: ItemBase):
    item = item_or_404(item_id)  # Check if item exists
    with engine.connect() as conn:
        conn.execute(update(items_table).where(items_table.c.id == item_id).values(
            name=new_item.name,
            color=new_item.color
        ))
        conn.commit()
    return {"updated": True}

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: ItemId):
    _ = item_or_404(item_id)  # Check if item exists
    with engine.connect() as conn:
        conn.execute(delete(items_table).where(items_table.c.id == item_id))
        conn.commit()
    return {"deleted": True}
