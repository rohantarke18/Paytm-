from sqlalchemy import func

from .database import SessionLocal
from .models import Transaction


def get_merchant_analytics():
    db = SessionLocal()

    try:
        total = db.query(Transaction).count()

        successful = (
            db.query(Transaction)
            .filter(Transaction.status == "success")
            .count()
        )

        failed = (
            db.query(Transaction)
            .filter(Transaction.status == "failed")
            .count()
        )

        total_revenue = (
            db.query(func.sum(Transaction.amount))
            .filter(Transaction.status == "success")
            .scalar()
            or 0
        )

        failed_value = (
            db.query(func.sum(Transaction.amount))
            .filter(Transaction.status == "failed")
            .scalar()
            or 0
        )

        failure_rate = (
            (failed / total) * 100
            if total > 0
            else 0
        )

        failure_reasons = (
            db.query(
                Transaction.failure_reason,
                func.count(Transaction.id)
            )
            .filter(Transaction.status == "failed")
            .group_by(Transaction.failure_reason)
            .all()
        )

        reasons = {
            reason: count
            for reason, count in failure_reasons
            if reason is not None
        }

        return {
            "total_transactions": total,
            "successful_transactions": successful,
            "failed_transactions": failed,
            "failure_rate_percent": round(failure_rate, 2),
            "successful_revenue": round(total_revenue, 2),
            "failed_transaction_value": round(failed_value, 2),
            "failure_reasons": reasons,
        }

    finally:
        db.close()


def get_anomaly_analysis():
    db = SessionLocal()

    try:
        transactions = (
            db.query(Transaction)
            .order_by(Transaction.id)
            .all()
        )

        if len(transactions) < 100:
            return {
                "error": "Not enough transactions for anomaly analysis."
            }

        # First 90% = historical baseline
        split_index = int(len(transactions) * 0.9)

        baseline = transactions[:split_index]
        recent = transactions[split_index:]

        baseline_failed = sum(
            1 for t in baseline
            if t.status == "failed"
        )

        recent_failed = sum(
            1 for t in recent
            if t.status == "failed"
        )

        baseline_rate = (
            baseline_failed / len(baseline) * 100
        )

        recent_rate = (
            recent_failed / len(recent) * 100
        )

        rate_increase = recent_rate - baseline_rate

        anomaly_detected = (
            recent_rate > baseline_rate * 2
        )

        return {
            "baseline_transactions": len(baseline),
            "baseline_failed": baseline_failed,
            "baseline_failure_rate_percent": round(
                baseline_rate, 2
            ),

            "recent_transactions": len(recent),
            "recent_failed": recent_failed,
            "recent_failure_rate_percent": round(
                recent_rate, 2
            ),

            "failure_rate_increase_percentage_points": round(
                rate_increase, 2
            ),

            "anomaly_detected": anomaly_detected,
        }

    finally:
        db.close()