from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from datetime import datetime

from .config import settings
from .models.schemas import HealthCheck, Message
from .routers import papers_router, search_router, users_router, external_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    description="""
    ## Paperly.utec - Sistema de Navegación de Papers

    Sistema de navegación de papers académicos diseñado para el departamento de Computer Science de UTEC. 
    
    ### Características principales:
    - 🔍 Búsqueda avanzada de papers académicos
    - 👤 Gestión de usuarios y autenticación
    - 📚 CRUD completo de papers
    - 🌐 Integración con repositorios externos (mock)
    - 📊 Sistema de búsqueda con caché
    
    ### Repositorios externos simulados:
    - arXiv
    - IEEE Xplore
    - ACM Digital Library
    
    ### Autenticación:
    Utiliza JWT tokens para autenticación. Primero registra un usuario y luego inicia sesión para obtener el token.
    """,
    version=settings.app_version,
    contact={
        "name": "Computer Science Department - UTEC",
        "email": "cs@utec.edu.pe",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log de request entrante
    logger.info(f"Incoming request: {request.method} {request.url}")
    
    # Procesar request
    response = await call_next(request)
    
    # Calcular tiempo de procesamiento
    process_time = time.time() - start_time
    
    # Log de response
    logger.info(f"Request completed: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.3f}s")
    
    return response

# Incluir routers
app.include_router(users_router)
app.include_router(papers_router)
app.include_router(search_router)
app.include_router(external_router)

# Endpoints principales
@app.get("/", response_model=Message, tags=["root"])
async def root():
    """
    Endpoint raíz que proporciona información básica de la API.
    """
    return Message(message=f"Bienvenido a {settings.app_name} v{settings.app_version}")

@app.get("/health", response_model=HealthCheck, tags=["health"])
async def health_check():
    """
    Endpoint de health check para verificar el estado del servicio.
    """
    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=settings.app_version
    )

@app.get("/info", tags=["info"])
async def get_api_info():
    """
    Información detallada sobre la API y sus capacidades.
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "Sistema de navegación de papers académicos",
        "features": [
            "Gestión de papers académicos",
            "Búsqueda avanzada",
            "Autenticación JWT",
            "Mock de APIs externas",
            "Documentación interactiva"
        ],
        "endpoints": {
            "documentation": "/docs",
            "alternative_docs": "/redoc",
            "health": "/health",
            "papers": "/api/v1/papers/",
            "search": "/api/v1/search/papers",
            "auth": "/api/v1/auth/",
            "external": "/api/v1/external/"
        },
        "mock_repositories": [
            "arXiv",
            "IEEE Xplore", 
            "ACM Digital Library"
        ]
    }

# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handler para errores 404"""
    logger.warning(f"404 Not Found: {request.method} {request.url}")
    return JSONResponse(
        status_code=404,
        content={"message": "Recurso no encontrado", "detail": "La URL solicitada no existe"}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handler para errores 500"""
    logger.error(f"500 Internal Server Error: {request.method} {request.url} - {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "Error interno del servidor", "detail": "Ha ocurrido un error inesperado"}
    )

# Crear directorio de logs al iniciar
import os
os.makedirs("logs", exist_ok=True)

# Log de inicio de la aplicación
logger.info(f"Starting {settings.app_name} v{settings.app_version}")
logger.info(f"Debug mode: {settings.debug}")
logger.info(f"Mock APIs enabled: {settings.mock_enabled}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
