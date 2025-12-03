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
    return templates.TemplateResponse("index.html", {"request": request, "page": "home"})


@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "page": "register"})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "page": "login"})

@app.get("/account")
async def account_page(request: Request):
    return templates.TemplateResponse("account.html", {"request": request, "page": "account"})

@app.post("/create")
async def create_post(
    request: Request,
    text: str = "TEXT",
    bg_color: str = "#ffffff",
    text_color: str = "#000000"
):
    hash_id = generate(size=8)
    full_url = f"http://localhost:8000/{hash_id}"
    
    return f"""
    <div class="glass-card rounded-xl p-6 bg-green-50 border border-green-200 animate-fade-in">
      <div class="flex items-start gap-3">
        <div class="mt-1">
          <i class="fas fa-check-circle text-green-500 text-xl"></i>
        </div>
        <div>
          <h3 class="font-bold text-lg text-green-800">Пост создан!</h3>
          <p class="mt-1 text-green-700">Ваш уникальный URL:</p>
          <div class="mt-2 bg-white rounded-lg p-3 border border-gray-200">
            <code class="font-mono text-sm break-all">{full_url}</code>
          </div>
          <p class="mt-2 text-sm text-green-600">
            <i class="fas fa-clock mr-1"></i> Пост будет доступен 24 часа
          </p>
          <div class="mt-4 flex gap-3">
            <button id="copy-btn" class="px-4 py-2 bg-green-100 text-green-800 rounded-lg hover:bg-green-200 transition flex items-center gap-1">
              <i class="fas fa-copy mr-1"></i> Скопировать
            </button>
            <a href="/{hash_id}" target="_blank"
              class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition flex items-center gap-1">
              <i class="fas fa-external-link-alt mr-1"></i> Открыть
            </a>
          </div>
        </div>
      </div>
    </div>
    <script>
      document.getElementById('copy-btn').addEventListener('click', function() {{
        navigator.clipboard.writeText('{full_url}');
        this.innerHTML = '<i class="fas fa-check mr-1"></i> Скопировано!';
        this.classList.replace('bg-green-100', 'bg-green-200');
      }});
      
      // Автоматическое копирование через 2 секунды
      setTimeout(() => {{
        navigator.clipboard.writeText('{full_url}');
        const btn = document.getElementById('copy-btn');
        btn.innerHTML = '<i class="fas fa-check mr-1"></i> Скопировано!';
        btn.classList.replace('bg-green-100', 'bg-green-200');
      }}, 2000);
    </script>
    """



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8080, host="127.0.0.1")
