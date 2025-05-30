import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)
logger.info("Starting Journal Reflection API...")

app = FastAPI(
    title="Journal Entry AI Reflection App",
    description="Submit your journal entry and receive an AI-powered reflection and affirmation.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api", tags=["journal"])


