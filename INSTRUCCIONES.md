# Paperly.utec - Instrucciones de Ejecución

## 🚀 Inicio Rápido

### Opción 1: Script Automático (Windows)
```bash
# Ejecutar el script de setup (instala todo automáticamente)
setup.bat

# Iniciar el servidor
run_server.bat
```

### Opción 2: Manual
```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual (Windows)
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear directorios necesarios
mkdir data
mkdir logs

# 5. Inicializar base de datos con datos de ejemplo
python init_db.py

# 6. Iniciar servidor
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Acceso a la Documentación

Una vez iniciado el servidor, accede a:

- **Documentación Interactiva (Swagger)**: http://localhost:8000/docs
- **Documentación Alternativa (ReDoc)**: http://localhost:8000/redoc
- **API Info**: http://localhost:8000/info
- **Health Check**: http://localhost:8000/health

## 👤 Usuarios de Prueba

El script `init_db.py` crea usuarios de ejemplo:

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | Administrador |
| researcher1 | research123 | Investigador |
| student1 | student123 | Estudiante |

## 🧪 Pruebas de la API

### 1. Registrar nuevo usuario
```bash
POST /api/v1/auth/register
{
  "username": "nuevouser",
  "email": "nuevo@utec.edu.pe",
  "password": "password123",
  "full_name": "Nuevo Usuario"
}
```

### 2. Iniciar sesión
```bash
POST /api/v1/auth/login
{
  "username": "admin",
  "password": "admin123"
}
```

### 3. Crear paper
```bash
POST /api/v1/papers/
{
  "title": "Mi Nuevo Paper",
  "abstract": "Descripción del paper...",
  "authors": ["Autor 1", "Autor 2"],
  "publication_year": 2024,
  "keywords": ["machine learning", "AI"]
}
```

### 4. Buscar papers
```bash
GET /api/v1/search/papers?q=machine learning&limit=5
```

### 5. Mock APIs externas
```bash
GET /api/v1/external/papers?q=deep learning
GET /api/v1/external/arxiv?q=computer vision
GET /api/v1/external/ieee?q=cybersecurity
```

## 🔧 Ejecutar Tests
```bash
# Activar entorno virtual
venv\Scripts\activate

# Ejecutar tests
pytest tests/ -v
```

## 📊 Características Implementadas

✅ **Gestión de Papers**
- CRUD completo de papers
- Búsqueda por título y contenido
- Búsqueda por autor
- Papers populares por citation count

✅ **Autenticación**
- Registro de usuarios
- Login con JWT tokens
- Protección de endpoints

✅ **Mock APIs Externas**
- Simulación de arXiv
- Simulación de IEEE Xplore 
- Simulación de ACM Digital Library

✅ **Funcionalidades Adicionales**
- Cache simple en memoria
- Logging de búsquedas
- Sugerencias de búsqueda
- Health checks
- Documentación interactiva completa

## 🎯 Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/docs` | GET | Documentación Swagger |
| `/health` | GET | Health check |
| `/api/v1/auth/register` | POST | Registrar usuario |
| `/api/v1/auth/login` | POST | Iniciar sesión |
| `/api/v1/papers/` | GET/POST | Listar/crear papers |
| `/api/v1/papers/{id}` | GET/PUT/DELETE | Operaciones específicas |
| `/api/v1/search/papers` | GET | Buscar papers |
| `/api/v1/search/authors` | GET | Buscar por autor |
| `/api/v1/external/papers` | GET | Mock repositorios externos |

## 💡 Notas Importantes

- La base de datos SQLite se crea en `data/paperly.db`
- Los logs se guardan en `logs/app.log`
- El servidor se ejecuta en `http://localhost:8000`
- La documentación Swagger está disponible automáticamente
- Todos los endpoints están documentados con ejemplos

¡La implementación está completa y lista para usar! 🎉
