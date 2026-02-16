from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import user
from app.models import conversation
from app.models import profile

from app.routes import auth
from app.routes import protected
from app.routes import memory
from app.routes import chat
from app.routes import admin


app = FastAPI()

# ===============================
# CORS Configuration (IMPORTANT)
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# Create Database Tables
# ===============================
user.Base.metadata.create_all(bind=engine)

# ===============================
# Include Routes
# ===============================
app.include_router(auth.router)
app.include_router(protected.router)
app.include_router(memory.router)
app.include_router(chat.router)
app.include_router(admin.router)


# ===============================
# Root Endpoint
# ===============================
@app.get("/")
def read_root():
    return {"message": "AI Personal Assistant Backend is running 🚀"}
