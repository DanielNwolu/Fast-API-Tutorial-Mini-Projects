import uvicorn
from fastapi import FastAPI
from routes import index

app =FastAPI()

PORT = 8001

@app.get("/")
async def read_root():
    return {"message": "Hello, World"}
   
app.include_router(index.router)