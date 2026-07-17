from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.logger import logger
from fastapi import Request
from fastapi.responses import JSONResponse
from routes.auth import router as auth_router
from routes.tenants import router as tenant_router
from routes.users import (
    router as users_router
)
from routes.dashboard import (
    router as dashboard_router
)
from routes.organization import (
    router as organization_router
)


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
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    tenant_router
)
app.include_router(
    users_router
)


app.include_router(
    dashboard_router
)


app.include_router(
    organization_router
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





