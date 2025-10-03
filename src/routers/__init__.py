# API Routers
from .papers import router as papers_router
from .search import router as search_router
from .users import router as users_router
from .external import router as external_router

__all__ = ["papers_router", "search_router", "users_router", "external_router"]
