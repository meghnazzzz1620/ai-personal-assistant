from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.utils.auth import get_current_user, get_db
from app.models.user import User
from app.models.conversation import Conversation

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/analytics")
def get_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Simple admin check
    if current_user.id != 1:
        raise HTTPException(status_code=403, detail="Admin access only")

    total_users = db.query(User).count()
    total_messages = db.query(Conversation).count()

    # Messages grouped per user_id
    grouped = (
        db.query(
            Conversation.user_id,
            func.count(Conversation.id)
        )
        .group_by(Conversation.user_id)
        .all()
    )

    messages_per_user = []

    for user_id, count in grouped:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            messages_per_user.append({
                "email": user.email,
                "count": count
            })

    most_active_user = max(
        messages_per_user,
        key=lambda x: x["count"],
        default=None
    )

    return {
        "total_users": total_users,
        "total_messages": total_messages,
        "total_conversations": len(grouped),
        "messages_per_user": messages_per_user,
        "most_active_user": most_active_user
    }
