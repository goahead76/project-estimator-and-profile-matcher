# main.py - Complete Unified Server Entrypoint Configuration

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import estimator

app = FastAPI(title="Project Estimator & Profile Matcher")

# 1. Mount static folders for local assets like charts
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. CORS Middleware configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 3. Mount modular route controllers
app.include_router(estimator.router)

# 4. Root Endpoint to serve Main Frontend landing page
@app.get("/")
def read_root():
    return FileResponse("index.html")

# =====================================================================
# ADD THIS NEW ROUTE HERE TO MAP YOUR SECONDARY PAGE CORRECTLY:
# =====================================================================
@app.get("/analytics.html")
def read_analytics_dashboard():
    """
    Acts as a secure user interface delivery layer, returning your static 
    analytics.html template file straight to client browsers when requested.
    """
    return FileResponse("analytics.html")
