# Paperly.utec - Sistema de Navegación de Papers

## Descripción del Proyecto

Paperly.utec es un sistema de navegación de papers académicos diseñado para el departamento de Computer Science de UTEC. El sistema permite buscar, visualizar, descargar y gestionar papers académicos mediante una arquitectura de microservicios robusta y escalable.

## Arquitectura de Software

El sistema está diseñado siguiendo un patrón de arquitectura de microservicios con los siguientes componentes principales:

### Componentes Core

- **API Gateway**: Punto de entrada único para todas las solicitudes
- **Load Balancer**: Distribución de carga entre servicios
- **Monitoring Service**: Monitoreo del sistema
- **Notification Service**: Gestión de notificaciones

### Servicios de Dominio

- **Paper Service**: Gestión central de papers
- **Search Service**: Motor de búsqueda de papers
- **User Profile Service**: Gestión de perfiles de usuario
- **Recommendation Service**: Sistema de recomendaciones
- **Analytics Service**: Análisis de datos y métricas
- **Download Service**: Gestión de descargas de papers
- **Logging Service**: Registro de eventos del sistema

### Servicios de Soporte

- **Auth Service**: Autenticación y autorización
- **Rank Service**: Sistema de ranking de papers
- **Information Extract Service**: Extracción de información de papers
- **Publisher Service**: Gestión de editores
- **Preview Service**: Vista previa de papers

## Stack Tecnológico

### Backend

- **Lenguaje Principal**: Python 3.9+
- **Framework Web**: FastAPI
- **API Documentation**: Swagger/OpenAPI (automático con FastAPI)
- **Validation**: Pydantic (integrado con FastAPI)

### Base de Datos (Simplificada)

- **Base de Datos Principal**: SQLite (para desarrollo local)
- **Cache**: Memoria local (diccionarios Python) o Redis local opcional
- **Búsqueda**: Búsqueda simple con SQL LIKE o whoosh (librería Python)

### Infraestructura Local

- **Containerización**: Docker (opcional, solo para bases de datos)
- **Servidor Web**: Uvicorn (incluido con FastAPI)
- **Proxy Reverso**: No necesario para desarrollo local
- **Comunicación entre servicios**: HTTP requests simples

### Monitoring Local

- **Logging**: Python logging estándar con archivos locales
- **Health Checks**: Endpoints `/health` simples
- **Metrics**: Logs básicos y contadores en memoria

### Patrones de Arquitectura Implementados (Simplificados)

- **Separación de Responsabilidades**: Cada servicio en su propio módulo Python
- **RESTful APIs**: Endpoints claros y semánticos
- **Configuration Management**: Variables de entorno y archivos .env
- **Simple Caching**: Cache en memoria para datos frecuentes
- **Error Handling**: Manejo básico de excepciones con FastAPI

## API External Repositories (Mock)

### Servicios Externos Simulados

- **ResearchGate API Mock**: Simulación de papers de ResearchGate
- **OpenSearch API Mock**: Simulación de búsquedas académicas
- **Auth Viewing Mock**: Simulación de autorización de visualización
- **Hyperlink Service Mock**: Simulación de servicios de enlaces

### Implementación del Mock (Local)

```python
# Mock simple con datos en memoria
class ExternalRepositoryMock:
    def __init__(self):
        self.papers_data = [
            {"id": 1, "title": "Sample Paper 1", "authors": ["Author 1"]},
            {"id": 2, "title": "Sample Paper 2", "authors": ["Author 2"]},
        ]
    
    def search_papers(self, query: str):
        # Búsqueda simple en memoria
        return [p for p in self.papers_data if query.lower() in p["title"].lower()]
```

## Estructura del Proyecto (Simplificada)

```
paperly-utec/
├── src/
│   ├── main.py                 # FastAPI app principal
│   ├── models/                 # Modelos SQLAlchemy
│   ├── services/              # Lógica de negocio
│   │   ├── paper_service.py
│   │   ├── search_service.py
│   │   ├── user_service.py
│   │   └── mock_external_api.py
│   ├── routers/               # Endpoints FastAPI
│   │   ├── papers.py
│   │   ├── search.py
│   │   └── users.py
│   ├── database/              # Configuración BD
│   │   ├── connection.py
│   │   └── models.py
│   └── config.py              # Configuración
├── data/                      # Archivos SQLite
├── tests/                     # Tests simples
├── requirements.txt           # Dependencias Python
├── .env                       # Variables de entorno
└── README.md
```

## Tecnologías por Servicio (Simplificadas)

### Paper Service (FastAPI + Python)
- **Framework**: FastAPI
- **ORM**: SQLAlchemy (con SQLite)
- **Database**: SQLite local
- **Validation**: Pydantic

### Search Service (FastAPI + Python)
- **Search Engine**: Búsqueda SQL simple con LIKE
- **Framework**: FastAPI
- **Database**: SQLite (misma que papers)
- **Cache**: Diccionario Python en memoria

### User Service (FastAPI + Python)
- **Framework**: FastAPI
- **Database**: SQLite
- **Authentication**: JWT simple
- **Password Hashing**: passlib con bcrypt

### Mock External API (FastAPI + Python)
- **Framework**: FastAPI
- **Data Storage**: Lista/diccionarios Python en memoria
- **Response Format**: JSON simple

### Analytics Service (Opcional)
- **Framework**: FastAPI
- **Data**: Logs en archivos de texto
- **Processing**: Funciones Python básicas

## Instalación y Configuración (Local)

### Prerrequisitos

- Python 3.9+
- pip (gestor de paquetes Python)

### Variables de Entorno (.env)

```bash
# Database local
DATABASE_URL=sqlite:///./data/paperly.db

# JWT Configuration
JWT_SECRET_KEY=tu-clave-secreta-local
JWT_ALGORITHM=HS256

# Mock API
MOCK_ENABLED=true
```

### Comandos de Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd paperly-utec

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear directorio para base de datos
mkdir data

# Ejecutar migraciones (crear tablas)
python -c "from src.database.connection import create_tables; create_tables()"

# Iniciar servidor
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Requirements.txt (Dependencias Mínimas)

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
```

## API Endpoints Principales

Una vez iniciado el servidor en `http://localhost:8000`, podrás acceder a:

- **Documentación Interactiva**: `http://localhost:8000/docs` (Swagger UI)
- **Documentación Alternativa**: `http://localhost:8000/redoc`

### Paper Service
- `GET /api/v1/papers/` - Listar todos los papers
- `GET /api/v1/papers/{id}` - Obtener paper específico
- `POST /api/v1/papers/` - Crear nuevo paper
- `PUT /api/v1/papers/{id}` - Actualizar paper

### Search Service
- `GET /api/v1/search/papers?q={query}` - Buscar papers por título
- `GET /api/v1/search/authors?q={query}` - Buscar por autor

### User Service
- `POST /api/v1/auth/register` - Registrar nuevo usuario
- `POST /api/v1/auth/login` - Iniciar sesión
- `GET /api/v1/users/profile` - Obtener perfil (requiere token)

### Mock External API
- `GET /api/v1/external/papers` - Simular búsqueda en repositorios externos

## Testing (Simplificado)

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest tests/ -v

# Tests básicos incluidos:
# - Test de endpoints
# - Test de autenticación
# - Test del mock de API externa
```

## Deployment Local

```bash
# Ejecutar en modo desarrollo
uvicorn src.main:app --reload --port 8000

# Ejecutar en modo producción local
uvicorn src.main:app --host 0.0.0.0 --port 8000

# Verificar que funciona
curl http://localhost:8000/health
```

## Monitoreo Local

- **Health Check**: `GET /health` - Verifica estado del servicio
- **Logs**: Archivos en `logs/app.log` con rotación diaria
- **Métricas básicas**: Contador de requests en memoria
- **Debug**: Logs detallados en modo desarrollo

## Primeros Pasos

1. **Instalar y ejecutar**:
   ```bash
   pip install -r requirements.txt
   uvicorn src.main:app --reload
   ```

2. **Probar la API**:
   - Ir a `http://localhost:8000/docs`
   - Registrar un usuario
   - Crear algunos papers
   - Probar búsquedas

3. **Verificar el mock**:
   - `GET /api/v1/external/papers`
   - Debería retornar papers simulados

## Escalabilidad Futura

Este setup local puede evolucionar gradualmente:
- SQLite → PostgreSQL
- Cache en memoria → Redis
- Búsqueda simple → Elasticsearch
- Un solo proceso → Múltiples servicios
- Variables locales → Docker containers

## Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## Contacto

- **Equipo de Desarrollo**: Computer Science Department - UTEC
- **Arquitecto de Software**: [Tu nombre]
- **Email**: [email@utec.edu.pe]

---

**Nota**: Este proyecto implementa un sistema completo de navegación de papers académicos con arquitectura de microservicios, diseñado específicamente para las necesidades del departamento de Computer Science de UTEC.
