from sqlalchemy import func

from .database import SessionLocal
from .models import Transaction


db = SessionLocal()

try:
    total = db.query(Transaction).count()

    failed = (
        db.query(Transaction)
        .filter(Transaction.status == "failed")
        .count()
    )

    successful = (
        db.query(Transaction)
        .filter(Transaction.status == "success")
        .count()
    )

    failure_rate = (failed / total) * 100 if total else 0

    print("\n===== MERCHANT DATA HEALTH =====")
    print(f"Total transactions : {total}")
    print(f"Successful         : {successful}")
    print(f"Failed             : {failed}")
    print(f"Failure rate       : {failure_rate:.2f}%")

    print("\n===== FAILURE REASONS =====")

    reasons = (
        db.query(
            Transaction.failure_reason,
            func.count(Transaction.id)
        )
        .filter(Transaction.status == "failed")
        .group_by(Transaction.failure_reason)
        .all()
    )

    for reason, count in reasons:
        print(f"{reason}: {count}")

finally:
    db.close()