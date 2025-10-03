from ..models.schemas import ExternalPaper, ExternalSearchResponse
from typing import List
import random

class ExternalRepositoryMock:
    """Mock de APIs externas de repositorios académicos"""
    
    def __init__(self):
        # Datos de ejemplo para simular repositorios externos
        self.arxiv_papers = [
            {
                "id": "arxiv:2401.00001",
                "title": "Advances in Deep Learning for Computer Vision",
                "authors": ["John Smith", "Jane Doe"],
                "abstract": "This paper presents novel advances in deep learning techniques for computer vision applications.",
                "source": "arxiv",
                "url": "https://arxiv.org/abs/2401.00001"
            },
            {
                "id": "arxiv:2401.00002", 
                "title": "Natural Language Processing with Transformers",
                "authors": ["Alice Johnson", "Bob Wilson"],
                "abstract": "An comprehensive review of transformer models in NLP applications.",
                "source": "arxiv",
                "url": "https://arxiv.org/abs/2401.00002"
            }
        ]
        
        self.ieee_papers = [
            {
                "id": "ieee:2024.001",
                "title": "Quantum Computing Applications in Cryptography",
                "authors": ["Dr. Maria Garcia", "Prof. David Chen"],
                "abstract": "Exploring the impact of quantum computing on modern cryptographic systems.",
                "source": "ieee",
                "url": "https://ieeexplore.ieee.org/document/2024001"
            },
            {
                "id": "ieee:2024.002",
                "title": "IoT Security Framework for Smart Cities",
                "authors": ["Sarah Brown", "Michael Davis"],
                "abstract": "A comprehensive security framework for IoT devices in smart city environments.",
                "source": "ieee", 
                "url": "https://ieeexplore.ieee.org/document/2024002"
            }
        ]
        
        self.acm_papers = [
            {
                "id": "acm:2024.001",
                "title": "Blockchain Technology in Supply Chain Management",
                "authors": ["Robert Taylor", "Emma Wilson"],
                "abstract": "Implementation of blockchain for transparent supply chain tracking.",
                "source": "acm",
                "url": "https://dl.acm.org/doi/10.1145/3024001"
            }
        ]
    
    def search_arxiv(self, query: str, limit: int = 5) -> ExternalSearchResponse:
        """Simular búsqueda en arXiv"""
        matching_papers = [
            paper for paper in self.arxiv_papers 
            if query.lower() in paper["title"].lower() or query.lower() in paper["abstract"].lower()
        ]
        
        # Si no hay coincidencias exactas, devolver algunos papers aleatorios
        if not matching_papers:
            matching_papers = random.sample(self.arxiv_papers, min(len(self.arxiv_papers), limit))
        
        papers = [ExternalPaper(**paper) for paper in matching_papers[:limit]]
        
        return ExternalSearchResponse(
            query=query,
            source="arxiv",
            total=len(papers),
            papers=papers
        )
    
    def search_ieee(self, query: str, limit: int = 5) -> ExternalSearchResponse:
        """Simular búsqueda en IEEE Xplore"""
        matching_papers = [
            paper for paper in self.ieee_papers 
            if query.lower() in paper["title"].lower() or query.lower() in paper["abstract"].lower()
        ]
        
        if not matching_papers:
            matching_papers = random.sample(self.ieee_papers, min(len(self.ieee_papers), limit))
            
        papers = [ExternalPaper(**paper) for paper in matching_papers[:limit]]
        
        return ExternalSearchResponse(
            query=query,
            source="ieee",
            total=len(papers),
            papers=papers
        )
    
    def search_acm(self, query: str, limit: int = 5) -> ExternalSearchResponse:
        """Simular búsqueda en ACM Digital Library"""
        matching_papers = [
            paper for paper in self.acm_papers 
            if query.lower() in paper["title"].lower() or query.lower() in paper["abstract"].lower()
        ]
        
        if not matching_papers:
            matching_papers = random.sample(self.acm_papers, min(len(self.acm_papers), limit))
            
        papers = [ExternalPaper(**paper) for paper in matching_papers[:limit]]
        
        return ExternalSearchResponse(
            query=query,
            source="acm",
            total=len(papers),
            papers=papers
        )
    
    def search_all_sources(self, query: str, limit_per_source: int = 3) -> List[ExternalSearchResponse]:
        """Buscar en todas las fuentes externas"""
        results = []
        
        results.append(self.search_arxiv(query, limit_per_source))
        results.append(self.search_ieee(query, limit_per_source))
        results.append(self.search_acm(query, limit_per_source))
        
        return results

# Instancia global del mock
external_api_mock = ExternalRepositoryMock()
