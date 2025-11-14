# FastAPI Entry Point - LokaFit Backend Server

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import scan, profile, recommend
import numpy
print("NumPy version:", numpy.__version__)

app = FastAPI(
    title="LokaFit API",
    description="AI-powered fashion stylist backend",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(scan.router, prefix="/api/v1/scan", tags=["scan"])
app.include_router(profile.router, prefix="/api/v1/profile", tags=["profile"])
app.include_router(recommend.router, prefix="/api/v1/recommend", tags=["recommend"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "lokafit-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
