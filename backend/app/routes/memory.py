from fastapi import APIRouter, Depends
from app.utils.auth import get_current_user
from app.models.user import User
from app.services.vector_instance import get_user_vector_store

router = APIRouter()

@router.post("/memory/add")
def add_memory(
    text: str,
    current_user: User = Depends(get_current_user)
):
    vector_store = get_user_vector_store(current_user.id)
    vector_store.add_text(text)
    return {"message": "Text added to your memory"}

@router.get("/memory/search")
def search_memory(
    query: str,
    current_user: User = Depends(get_current_user)
):
    vector_store = get_user_vector_store(current_user.id)
    results = vector_store.search(query)
    return {"results": results}
