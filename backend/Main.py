from fastapi import FastAPI
from backend.Api.agents import router as agents_router
from backend.Api.chat import router as chat_router

app = FastAPI(
    title="PeriMatrix AI",
    description="Backend API for the PeriMatrix AI platform.",
    version="0.1.0",
)

# Register the AI agent collaboration squad routes
app.include_router(agents_router)
app.include_router(chat_router)

@app.get("/")
def root():
    return {
        "name": "PeriMatrix AI",
        "status": "online",
        "version": app.version,
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
