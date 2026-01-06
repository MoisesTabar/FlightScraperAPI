from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper.router import router as scraper_router
from voice.router import router as voice_router
from text.router import router as text_router
from middleware import register_exception_handlers

app = FastAPI(
    title="Flight Search API",
    description="API for voice and text-based flight search",
    version="1.0.0"
)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(scraper_router, prefix='/flights')
app.include_router(voice_router, prefix='/flights')
app.include_router(text_router, prefix='/flights')
