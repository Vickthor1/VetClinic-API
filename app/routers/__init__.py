from app.routers.animals import router as animals_router
from app.routers.appointments import router as appointments_router
from app.routers.prescriptions import router as prescriptions_router
from app.routers.tutors import router as tutors_router
from app.routers.veterinarians import router as veterinarians_router

__all__ = [
    "animals_router",
    "appointments_router",
    "prescriptions_router",
    "tutors_router",
    "veterinarians_router",
]
