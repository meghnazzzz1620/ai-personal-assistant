from app.services.vector_store import VectorStore
from app.models.conversation import Conversation
from app.database import SessionLocal

# Store vector stores per user
user_vector_stores = {}

def rebuild_user_vector_store(user_id: int):
    db = SessionLocal()
    conversations = db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).all()

    vector_store = VectorStore()

    for convo in conversations:
        vector_store.add_text(convo.content)

    db.close()

    return vector_store


def get_user_vector_store(user_id: int):
    # If user vector store doesn't exist → rebuild from DB
    if user_id not in user_vector_stores:
        user_vector_stores[user_id] = rebuild_user_vector_store(user_id)

    return user_vector_stores[user_id]
