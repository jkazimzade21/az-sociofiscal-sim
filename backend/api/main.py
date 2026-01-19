"""
FastAPI Application for Azerbaijan Simplified Tax Calculator.

This is the main entry point for the API server.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .routes import simplified_tax_router
from .schemas.responses import HealthResponse


def get_cors_origins() -> list[str]:
    """Get CORS origins from environment or use defaults."""
    env_origins = os.environ.get("CORS_ORIGINS", "")
    if env_origins:
        return [origin.strip() for origin in env_origins.split(",") if origin.strip()]
    return [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://frontend:3000",
    ]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print(f"Starting Azerbaijan Simplified Tax Calculator API v{__version__}")
    yield
    # Shutdown
    print("Shutting down API...")


app = FastAPI(
    title="Azerbaijan Simplified Tax Calculator",
    description="""
    API for evaluating simplified tax eligibility and calculating tax amounts
    based on the Azerbaijan Tax Code.

    ## Features

    - **Eligibility Evaluation**: Check if a taxpayer qualifies for simplified tax
    - **Tax Calculation**: Calculate the simplified tax amount based on route
    - **Server-Driven Interview**: Step-by-step questionnaire for data collection
    - **Legal Traceability**: All rules linked to Tax Code article numbers

    ## Legal Sources

    - Tax Code: https://taxes.gov.az/az/page/vergi-mecellesi
    - License Law: https://president.az/az/documents/licenses

    ## Debug Mode

    Add `?debug=1` to the evaluate endpoint to include the full rule trace.
    """,
    version=__version__,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(simplified_tax_router)


@app.get("/", response_model=HealthResponse)
async def root() -> HealthResponse:
    """Root endpoint - health check."""
    return HealthResponse(status="healthy", version=__version__)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="healthy", version=__version__)


# For running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
