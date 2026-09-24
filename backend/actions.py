from datetime import datetime

from .database import SessionLocal
from .models import AgentAction


def create_merchant_incident(
    title: str,
    description: str,
    severity: str = "high",
):
    db = SessionLocal()

    try:
        action = AgentAction(
            action_type="merchant_incident",
            title=title,
            description=description,
            status="pending_approval",
            created_at=datetime.now(),
        )

        db.add(action)
        db.commit()
        db.refresh(action)

        return {
            "action_id": action.id,
            "action_type": action.action_type,
            "title": action.title,
            "description": action.description,
            "severity": severity,
            "status": action.status,
            "created_at": action.created_at.isoformat(),
        }

    finally:
        db.close()