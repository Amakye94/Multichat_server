from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routes import router as api_router

app = FastAPI()

app.include_router(api_router)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
