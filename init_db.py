"""
Script para inicializar la base de datos con datos de ejemplo
"""
import sys
import os

# Agregar el directorio src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from sqlalchemy.orm import Session
from src.database.connection import engine, SessionLocal
from src.database.models import Base, User, Paper
from src.services.auth_service import get_password_hash
import json

def create_sample_data():
    """Crear datos de ejemplo en la base de datos"""
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        # Verificar si ya existen datos
        existing_user = db.query(User).first()
        if existing_user:
            print("La base de datos ya contiene datos. Saltando inicialización.")
            return
        
        # Crear usuarios de ejemplo
        users_data = [
            {
                "username": "admin",
                "email": "admin@utec.edu.pe",
                "password": "admin123",
                "full_name": "Administrador del Sistema"
            },
            {
                "username": "researcher1",
                "email": "researcher1@utec.edu.pe", 
                "password": "research123",
                "full_name": "Dr. Juan Pérez"
            },
            {
                "username": "student1",
                "email": "student1@utec.edu.pe",
                "password": "student123",
                "full_name": "María García"
            }
        ]
        
        created_users = []
        for user_data in users_data:
            hashed_password = get_password_hash(user_data["password"])
            db_user = User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=hashed_password
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            created_users.append(db_user)
            print(f"Usuario creado: {user_data['username']}")
        
        # Crear papers de ejemplo
        papers_data = [
            {
                "title": "Deep Learning Applications in Computer Vision",
                "abstract": "This paper explores the latest advancements in deep learning techniques applied to computer vision problems, including object detection, image classification, and semantic segmentation.",
                "authors": ["Dr. Juan Pérez", "Ana López", "Carlos Ruiz"],
                "publication_year": 2024,
                "doi": "10.1000/sample.2024.001",
                "pdf_url": "https://example.com/papers/deep-learning-cv.pdf",
                "keywords": ["deep learning", "computer vision", "neural networks", "object detection"],
                "citation_count": 15,
                "creator_id": created_users[1].id
            },
            {
                "title": "Natural Language Processing with Transformer Models",
                "abstract": "A comprehensive review of transformer architectures and their applications in various NLP tasks including machine translation, text summarization, and question answering.",
                "authors": ["María García", "Roberto Silva"],
                "publication_year": 2024,
                "doi": "10.1000/sample.2024.002", 
                "pdf_url": "https://example.com/papers/nlp-transformers.pdf",
                "keywords": ["natural language processing", "transformers", "BERT", "machine translation"],
                "citation_count": 23,
                "creator_id": created_users[2].id
            },
            {
                "title": "Quantum Computing Algorithms for Optimization Problems",
                "abstract": "This study presents novel quantum algorithms for solving complex optimization problems, demonstrating significant speedup over classical approaches.",
                "authors": ["Dr. Elena Vásquez", "Miguel Torres"],
                "publication_year": 2023,
                "doi": "10.1000/sample.2023.001",
                "pdf_url": "https://example.com/papers/quantum-optimization.pdf",
                "keywords": ["quantum computing", "optimization", "algorithms", "quantum algorithms"],
                "citation_count": 8,
                "creator_id": created_users[1].id
            },
            {
                "title": "Blockchain Technology in Supply Chain Management",
                "abstract": "An implementation study of blockchain technology for transparent and secure supply chain tracking in the food industry.",
                "authors": ["Carlos Mendoza", "Laura Fernández", "Diego Morales"],
                "publication_year": 2023,
                "doi": "10.1000/sample.2023.002",
                "pdf_url": "https://example.com/papers/blockchain-supply-chain.pdf",
                "keywords": ["blockchain", "supply chain", "transparency", "food industry"],
                "citation_count": 12,
                "creator_id": created_users[1].id
            },
            {
                "title": "Machine Learning for Cybersecurity Threat Detection",
                "abstract": "This paper proposes a machine learning framework for real-time detection and classification of cybersecurity threats in network traffic.",
                "authors": ["Sofía Ramírez", "Andrés Castillo"],
                "publication_year": 2024,
                "doi": "10.1000/sample.2024.003",
                "pdf_url": "https://example.com/papers/ml-cybersecurity.pdf",
                "keywords": ["machine learning", "cybersecurity", "threat detection", "network security"],
                "citation_count": 6,
                "creator_id": created_users[2].id
            },
            {
                "title": "Edge Computing Architectures for IoT Applications",
                "abstract": "A comprehensive analysis of edge computing architectures and their performance benefits for Internet of Things applications.",
                "authors": ["Fernando Gutiérrez", "Valentina Cruz"],
                "publication_year": 2024,
                "doi": "10.1000/sample.2024.004",
                "pdf_url": "https://example.com/papers/edge-computing-iot.pdf",
                "keywords": ["edge computing", "IoT", "architecture", "performance"],
                "citation_count": 9,
                "creator_id": created_users[1].id
            }
        ]
        
        for paper_data in papers_data:
            # Convertir listas a JSON
            authors_json = json.dumps(paper_data["authors"])
            keywords_json = json.dumps(paper_data["keywords"])
            
            db_paper = Paper(
                title=paper_data["title"],
                abstract=paper_data["abstract"],
                authors=authors_json,
                publication_year=paper_data["publication_year"],
                doi=paper_data["doi"],
                pdf_url=paper_data["pdf_url"],
                keywords=keywords_json,
                citation_count=paper_data["citation_count"],
                creator_id=paper_data["creator_id"]
            )
            db.add(db_paper)
            print(f"Paper creado: {paper_data['title']}")
        
        db.commit()
        print("\n✅ Base de datos inicializada con datos de ejemplo!")
        print("\n👤 Usuarios creados:")
        for user_data in users_data:
            print(f"  - {user_data['username']} / {user_data['password']}")
        
        print(f"\n📚 {len(papers_data)} papers creados")
        print("\n🚀 Puedes iniciar el servidor con: uvicorn src.main:app --reload")
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
