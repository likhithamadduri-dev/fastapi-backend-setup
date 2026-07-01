from fastapi import FastAPI
from routes.users import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from core.logger import logger
from fastapi import Request
from fastapi.responses import JSONResponse
from routes.auth import router as auth_router

app = FastAPI(
    title="AI SAAS PROJECT"
)

logger.info("Application Started")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    user_router,
    prefix="/users",
    tags=["Users"]
),

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.error(f"Exception occurred: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "message": str(exc)
        }
    )

@app.get("/")
def home():

    logger.info("Home API Called")

    return {
        "message": "Application Running"
    }

@app.get("/health")
def health():

    logger.info("Health API Called")

    return {
        "status": "healthy"
    }

@app.get("/version")
def version():

    logger.info("Version API Called")

    return {
        "version": "1.0.0"
    }

