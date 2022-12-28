from fastapi import APIRouter
from app.routes.brokers import router as brokers_router
from app.routes.portfolios import router as portfolios_router
from app.routes.tasks import router as tasks_router

router = APIRouter()
router.include_router(brokers_router, prefix="/brokers", tags=["brokers"])
router.include_router(
    portfolios_router, prefix="/portfolios", tags=["portfolios"])
router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
