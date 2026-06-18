from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.exceptions import AppException
from app.core.handlers import app_exception_handler, validation_exception_handler
from app.routers import (
    animals_router,
    appointments_router,
    prescriptions_router,
    tutors_router,
    veterinarians_router,
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API REST para gestão de clínica veterinária.",
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(tutors_router)
app.include_router(animals_router)
app.include_router(veterinarians_router)
app.include_router(appointments_router)
app.include_router(prescriptions_router)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
