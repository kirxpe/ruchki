from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional

app = FastAPI()

# Наше "хранилище" данных
db: Dict[int, Dict] = {}

class Item(BaseModel):
    name: str
    description: Optional[str] = None

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    item_id = len(db) + 1
    db[item_id] = item.model_dump()
    return {"id": item_id, **item.model_dump()}

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **db[item_id]}

@app.get("/items/", response_model=Dict[str, Item])
def read_items():
    return {str(k): v for k, v in db.items()}

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    stored_item = db[item_id]
    update_data = item.model_dump(exclude_unset=True)
    updated_item = {**stored_item, **update_data}
    db[item_id] = updated_item
    return {"id": item_id, **updated_item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return {"message": "Item deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)