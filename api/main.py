from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import scraping, data_analysis, database_management
from api.auth import authentication
from db.database import init_db

app = FastAPI(
    title="API Integrations for Web Scraping",
    description="Robust system for web scraping, data analysis, and database management",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_event():
    await init_db()

# Include routers
app.include_router(authentication.router)
app.include_router(scraping.router, prefix="/api/v1/scrape", tags=["Scraping"])
app.include_router(data_analysis.router, prefix="/api/v1/analysis", tags=["Analysis"])
app.include_router(database_management.router, prefix="/api/v1/data", tags=["Database"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
