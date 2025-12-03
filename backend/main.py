from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from nanoid import generate

import uvicorn


app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/",summary="main",tags=["Основная"])
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/create")
async def create_post(
    request: Request,
    text: str = "TEXT",
    bg_color: str = "#ffffff",
    text_color: str = "#000000"
):
    hash_id = generate(size=8)

    return f"""
    <div class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
      <p class="font-medium">Создан пост!</p>
      <p>Текст: {text[:20]}...</p>
      <p>Хеш: {hash_id}</p>
      <p>Цвета: фон {bg_color}, текст {text_color}</p>
    </div>
    """



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8080, host="127.0.0.1")
