from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import shutil

# Імпорти бази та моделей
from app.database import Base, engine
from app import models
from app.routers import auth, users, agents, purchases

# Ініціалізація FastAPI
app = FastAPI(
    title="Star Agents API",
    version="1.0.0",
    description="API для керування користувачами, агентами та покупками"
)

# Створюємо таблиці у БД
Base.metadata.create_all(bind=engine)

# Підключаємо роутери
app.include_router(auth.router, tags=["Auth"])
app.include_router(users.router, tags=["Users"])
app.include_router(agents.router, tags=["Agents"])
app.include_router(purchases.router, tags=["Purchases"])

# Jinja2 templates (залишаємо для інших сторінок)
templates = Jinja2Templates(directory="templates")

# === FRONTEND ROUTES ===
# Головна сторінка → login.html
@app.get("/", response_class=HTMLResponse)
def landing_page():
    return FileResponse("static/login.html")

# Редирект з /login на /
@app.get("/login")
def login_redirect():
    return RedirectResponse(url="/")

# Сторінка агентів → agents.html
@app.get("/agents", response_class=HTMLResponse)
def agents_page():
    return FileResponse("static/agents.html")

# Сторінка покупок → purchases.html
@app.get("/purchases", response_class=HTMLResponse)
def purchases_page():
    return FileResponse("static/purchases.html")

# Тестовий upload
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    with open(f"uploaded_{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"detail": f"File {file.filename} uploaded successfully"}

# Демонстраційні агенти
@app.get("/featured_agents")
def featured_agents():
    return [
        {"name": "SEO Agent", "skills": "SEO, Keywords, Analytics"},
        {"name": "Marketing Agent", "skills": "Ads, Social Media, Targeting"},
        {"name": "Analytics Agent", "skills": "Reports, BI, Forecasting"},
    ]
