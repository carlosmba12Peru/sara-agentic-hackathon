"""Main FastAPI application entrypoint for SARA (Cognitive Extortion Response Agent)."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1.cases import router as cases_router
from app.api.v1.webhooks import router as webhooks_router

# Configure root logger
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("sara.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("==========================================================")
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT} | Host: {settings.HOST}:{settings.PORT}")
    logger.info(f"Gemini Model: {settings.GEMINI_MODEL}")
    logger.info("==========================================================")
    yield
    logger.info("Shutting down SARA service...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Multi-agent cognitive ecosystem for automated triage, forensic mitigation, "
        "and dynamic risk analysis (T_index) in extortion crimes."
    ),
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach API routers
app.include_router(cases_router, prefix="/api/v1")
app.include_router(webhooks_router, prefix="/api/v1")


@app.get("/healthz", tags=["System"])
async def health_check():
    """Health check endpoint for Google Cloud Run container liveness."""
    return {
        "status": "HEALTHY",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/", tags=["System"])
async def root():
    """Root metadata and welcome endpoint."""
    return {
        "project": "SARA - Cognitive Extortion Response Agent",
        "hackathon": "All Things Agentic Hackathon",
        "documentation": "/docs",
        "health": "/healthz",
        "status": "ONLINE",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=(settings.ENVIRONMENT == "development"),
    )
