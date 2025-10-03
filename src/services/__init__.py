# Services layer
from .auth_service import verify_password, get_password_hash, create_access_token, verify_token
from .user_service import get_user_by_username, get_user_by_email, get_user_by_id, create_user, authenticate_user
from .paper_service import (
    get_papers, get_paper_by_id, get_paper_by_doi, create_paper, update_paper, delete_paper, 
    search_papers, get_popular_papers, convert_db_paper_to_schema
)
from .search_service import search_papers_service, search_authors_service, get_search_suggestions
from .mock_external_api import external_api_mock

__all__ = [
    "verify_password", "get_password_hash", "create_access_token", "verify_token",
    "get_user_by_username", "get_user_by_email", "get_user_by_id", "create_user", "authenticate_user",
    "get_papers", "get_paper_by_id", "get_paper_by_doi", "create_paper", "update_paper", "delete_paper",
    "search_papers", "get_popular_papers", "convert_db_paper_to_schema",
    "search_papers_service", "search_authors_service", "get_search_suggestions",
    "external_api_mock"
]
