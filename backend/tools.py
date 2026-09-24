from sqlalchemy import func

from .database import SessionLocal
from .models import Transaction


def get_recent_failure_analysis():
    db = SessionLocal()

    try:
        transactions = (
            db.query(Transaction)
            .order_by(Transaction.id.desc())
            .limit(100)
            .all()
        )

        total = len(transactions)

        failed = [
            transaction
            for transaction in transactions
            if transaction.status == "failed"
        ]

        failure_reasons = {}

        for transaction in failed:
            reason = transaction.failure_reason

            if reason:
                failure_reasons[reason] = (
                    failure_reasons.get(reason, 0) + 1
                )

        failed_value = sum(
            transaction.amount
            for transaction in failed
        )

        failure_rate = (
            len(failed) / total * 100
            if total
            else 0
        )

        return {
            "period_transactions": total,
            "failed_transactions": len(failed),
            "failure_rate_percent": round(
                failure_rate, 2
            ),
            "failed_transaction_value": round(
                failed_value, 2
            ),
            "failure_reasons": failure_reasons,
        }

    finally:
        db.close()