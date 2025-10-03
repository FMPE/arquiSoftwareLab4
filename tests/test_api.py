import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.database.models import Base
from src.database.connection import get_db

# Base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def client():
    """Cliente de pruebas para FastAPI"""
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_health_check(client):
    """Test del endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data

def test_root_endpoint(client):
    """Test del endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_api_info(client):
    """Test del endpoint de información"""
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "features" in data
    assert "endpoints" in data

def test_register_user(client):
    """Test de registro de usuario"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "full_name": "Test User"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login_user(client):
    """Test de login de usuario"""
    # Primero registrar usuario
    user_data = {
        "username": "loginuser",
        "email": "login@example.com", 
        "password": "loginpassword"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    # Luego hacer login
    login_data = {
        "username": "loginuser",
        "password": "loginpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_paper(client):
    """Test de creación de paper"""
    paper_data = {
        "title": "Test Paper",
        "abstract": "This is a test paper",
        "authors": ["Test Author"],
        "publication_year": 2024,
        "keywords": ["test", "paper"]
    }
    response = client.post("/api/v1/papers/", json=paper_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Paper"
    assert data["authors"] == ["Test Author"]

def test_list_papers(client):
    """Test de listado de papers"""
    response = client.get("/api/v1/papers/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_search_papers(client):
    """Test de búsqueda de papers"""
    # Crear un paper primero
    paper_data = {
        "title": "Machine Learning Research",
        "abstract": "A study on ML algorithms",
        "authors": ["ML Researcher"]
    }
    client.post("/api/v1/papers/", json=paper_data)
    
    # Buscar papers
    response = client.get("/api/v1/search/papers?q=Machine")
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "results" in data

def test_external_mock_api(client):
    """Test del mock de APIs externas"""
    response = client.get("/api/v1/external/papers?q=deep learning")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Debe retornar resultados del mock

def test_arxiv_mock(client):
    """Test específico del mock de arXiv"""
    response = client.get("/api/v1/external/arxiv?q=computer vision")
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "arxiv"
    assert "papers" in data

def test_search_suggestions(client):
    """Test de sugerencias de búsqueda"""
    response = client.get("/api/v1/search/suggestions?q=machine")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
