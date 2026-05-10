# my_api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

app = FastAPI(title="Student Demo API")

@app.get("/")
def read_welcome():
    return {"message": f"[{datetime.now().time()}] Welcome to a simple demo!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": str(datetime.now())}

@app.get("/info")
def get_info():
    return {
        "api_name": "Student Demo API",
        "version": "1.0.0",
        "description": "A simple API for learning RESTful principles"
    } 

# our in-memory "database" 
items = {}

# my_api/main.py
...

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "value": items[item_id]}

# my_api/main.py

...
@app.post("/items/{item_id}")
def create_item(item_id: int, value: str):
    if item_id in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item_id] = value
    return {"message": "Item created", "id": item_id, "value": value}

# my_api/main.py

...
@app.put("/items/{item_id}")
def update_item(item_id: int, value: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = value
    return {"message": "Item updated", "id": item_id, "value": value}

# my_api/main.py
...

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"message": "Item deleted", "id": item_id}

# New endpoint to dump all items
@app.get("/items-dump")
def items_dump():
    """
    Returns all items currently stored in memory.
    """
    return {"items": items}
    
# Pydantic model for request/response validation
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 1

# our in-memory "database" - now stores Item objects
items5 = {}

@app.post("/items5/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in items5:
        raise HTTPException(status_code=400, detail="Item already exists")
    items5[item_id] = item.dict()
    return {"message": "Item created", "id": item_id, "item": items5[item_id]}

@app.get("/items5/{item_id}")
def read_item(item_id: int):
    if item_id not in items5:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "item": items5[item_id]}

@app.put("/items5/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items5:
        raise HTTPException(status_code=404, detail="Item not found")
    # overwriting the entire item with the new data
    items5[item_id] = item.dict()
    return {"message": "Item updated", "id": item_id, "item": items5[item_id]}

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

@app.patch("/items5/{item_id}")
def partial_update_item(item_id: int, item: ItemUpdate):
    if item_id not in items5:
        raise HTTPException(status_code=404, detail="Item not found")

    existing_item = items5[item_id]
    # Only update fields that are provided
    update_data = item.dict(exclude_unset=True)
    existing_item.update(update_data)

    items5[item_id] = existing_item

    return {"message": "Item partially updated", "id": item_id, "item": items5[item_id]}

@app.get("/items5")
def list_items(skip: int = 0, limit: int = 10):
    """List all items with optional pagination"""
    item_list = list(items5.items())[skip:skip+limit]
    return {
        "total": len(items5),
        "skip": skip,
        "limit": limit,
        "items": {k: v for k, v in item_list}
    }

