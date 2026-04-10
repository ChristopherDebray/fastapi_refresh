from fastapi import FastAPI
from routes._system import router as system_router

app = FastAPI(
    title="Fastapi refresh",
)

app.include_router(system_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}