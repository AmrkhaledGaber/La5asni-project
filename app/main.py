from fastapi import FastAPI
from app.api.v1.routes import router
from app.services.database import init_db

app = FastAPI(
    title="La5asni - Document Analyzer",
    description="Summarize, Extract, and Generate Training Modules from Documents.",
    version="1.0.0",
)
init_db() 
app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to La5asni - Document Analyzer API"}
