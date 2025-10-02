"""
Script alternativo para inicializar la base de datos con manejo de errores mejorado
"""
import sys
import os

# Agregar el directorio src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def create_simple_data():
    """Crear datos de ejemplo con manejo robusto de errores"""
    
    try:
        from sqlalchemy.orm import Session
        from src.database.connection import engine, SessionLocal
        from src.database.models import Base, User, Paper
        import json
        import hashlib
        
        print("Iniciando creación de base de datos...")
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas exitosamente")
        
        # Crear sesión
        db = SessionLocal()
        
        try:
            # Verificar si ya existen datos
            existing_user = db.query(User).first()
            if existing_user:
                print("La base de datos ya contiene datos. Saltando inicialización.")
                return
            
            # Función simple de hash como fallback
            def simple_hash(password: str) -> str:
                return hashlib.sha256(password.encode()).hexdigest()
            
            # Crear usuarios de ejemplo con contraseñas simples
            users_data = [
                {
                    "username": "admin",
                    "email": "admin@utec.edu.pe",
                    "password": "admin123",
                    "full_name": "Administrador"
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
                try:
                    # Intentar usar el servicio de auth primero
                    from src.services.auth_service import get_password_hash
                    hashed_password = get_password_hash(user_data["password"])
                except Exception as e:
                    print(f"Error con bcrypt, usando hash simple: {e}")
                    hashed_password = simple_hash(user_data["password"])
                
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
            
            # Crear algunos papers de ejemplo
            papers_data = [
                {
                    "title": "Deep Learning Applications in Computer Vision",
                    "abstract": "This paper explores deep learning techniques for computer vision.",
                    "authors": ["Dr. Juan Pérez", "Ana López"],
                    "publication_year": 2024,
                    "doi": "10.1000/sample.2024.001",
                    "keywords": ["deep learning", "computer vision"],
                    "citation_count": 15,
                    "creator_id": created_users[1].id
                },
                {
                    "title": "Natural Language Processing with Transformers",
                    "abstract": "A review of transformer architectures in NLP tasks.",
                    "authors": ["María García", "Roberto Silva"],
                    "publication_year": 2024,
                    "doi": "10.1000/sample.2024.002", 
                    "keywords": ["nlp", "transformers"],
                    "citation_count": 23,
                    "creator_id": created_users[2].id
                },
                {
                    "title": "Machine Learning for Cybersecurity",
                    "abstract": "ML framework for cybersecurity threat detection.",
                    "authors": ["Sofía Ramírez", "Andrés Castillo"],
                    "publication_year": 2024,
                    "doi": "10.1000/sample.2024.003",
                    "keywords": ["machine learning", "cybersecurity"],
                    "citation_count": 6,
                    "creator_id": created_users[0].id
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
                    keywords=keywords_json,
                    citation_count=paper_data["citation_count"],
                    creator_id=paper_data["creator_id"]
                )
                db.add(db_paper)
                print(f"Paper creado: {paper_data['title']}")
            
            db.commit()
            print("\n✅ Base de datos inicializada exitosamente!")
            print("\n👤 Usuarios creados:")
            for user_data in users_data:
                print(f"  - {user_data['username']} / {user_data['password']}")
            
            print(f"\n📚 {len(papers_data)} papers creados")
            print("\n🚀 Puedes iniciar el servidor con:")
            print("   uvicorn src.main:app --reload")
            print("   o ejecutar: run_server.bat")
            
        except Exception as e:
            print(f"Error al crear datos: {e}")
            db.rollback()
            raise
        finally:
            db.close()
            
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Asegúrate de haber instalado las dependencias:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_simple_data()
