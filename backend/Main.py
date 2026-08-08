
from fastapi import FastAPI

app = FastAPI(
    title="PeriMatrix AI",
    description="Backend API for the PeriMatrix AI platform.",
    version="0.1.0",
)


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
