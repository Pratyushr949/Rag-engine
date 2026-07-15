import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from routes.upload import router as upload_router
from routes.chat import router as chat_router
from routes.reset import router as reset_router
from routes.health import router as health_router
from routes.knowledge import router as knowledge_router
from routes.network import router as network_router

from utils.logger import get_logger
from config.config import config

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing RAG Application...")
    logger.info("System ready to accept connections.")
    yield
    logger.info("Shutting down RAG Application...")
    logger.info("Shutdown complete.")

app = FastAPI(
    title="RAG Engine Production API",
    description="Enterprise-grade Document Ingestion and History-Aware Chat",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request Started: {request.method} {request.url.path}")
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request Completed: {request.method} {request.url.path} - Status: {response.status_code} - Duration: {process_time:.4f}s")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception on {request.method} {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Please contact support."},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation Error on {request.method} {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Invalid request parameters.", "errors": exc.errors()},
    )

# Mount Routers
app.include_router(upload_router, prefix="/api", tags=["Documents"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(knowledge_router, prefix="/api", tags=["Knowledge"])
app.include_router(network_router, prefix="/api", tags=["Knowledge Graph"])
app.include_router(reset_router, prefix="/api", tags=["System"])
app.include_router(health_router, tags=["System"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host=config.HOST, port=config.PORT, reload=True)
