from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_memory_agent.config import settings
from ai_memory_agent.api.routes import router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "AI Security Operations & Compliance Memory Agent powered by Hindsight. "
        "Transforms episodic security incidents into persistent organizational memory "
        "to accelerate future investigations and ensure continuous audit readiness."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for Frontend UI (React, Vite, Vue, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", summary="Root Endpoint")
def root():
    return {
        "message": "AI Security Operations & Compliance Memory Agent API is online.",
        "documentation": "/docs",
        "health": "/api/health",
        "demo_story": "POST /api/demo/run-story",
    }
