from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import router
app = FastAPI()

@app.get("/")
async def read_root():
    return RedirectResponse(url="docs#")

app.include_router(router)