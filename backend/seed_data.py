from datetime import datetime, timedelta
import random

from faker import Faker

from .database import SessionLocal
from .models import Transaction


fake = Faker()


PAYMENT_METHODS = ["UPI", "Card", "Wallet"]

NORMAL_FAILURE_REASONS = [
    "insufficient_funds",
    "card_expired",
    "invalid_payment_details",
]

ANOMALY_FAILURE_REASONS = [
    "network_error",
    "payment_gateway_timeout",
    "processor_error",
]


def generate_transactions(count=1000):
    db = SessionLocal()

    try:
        # Remove old demo data so we can safely run this script again.
        db.query(Transaction).delete()

        now = datetime.now()

        for i in range(count):
            # First 900 = normal business activity
            # Last 100 = anomaly period
            is_anomaly = i >= 900

            customer_id = random.randint(1, 250)
            amount = round(random.uniform(100, 2500), 2)
            payment_method = random.choice(PAYMENT_METHODS)

            if is_anomaly:
                # Deliberately create a payment failure spike.
                is_failed = random.random() < 0.25
            else:
                # Normal failure rate.
                is_failed = random.random() < 0.04

            if is_failed:
                status = "failed"

                if is_anomaly:
                    failure_reason = random.choice(
                        ANOMALY_FAILURE_REASONS
                    )
                else:
                    failure_reason = random.choice(
                        NORMAL_FAILURE_REASONS
                    )
            else:
                status = "success"
                failure_reason = None

            timestamp = now - timedelta(
                minutes=(count - i) * 5
            )

            transaction = Transaction(
                customer_id=customer_id,
                amount=amount,
                status=status,
                failure_reason=failure_reason,
                payment_method=payment_method,
                timestamp=timestamp,
            )

            db.add(transaction)

        db.commit()

        print(f"Created {count} synthetic transactions.")

    finally:
        db.close()


if __name__ == "__main__":
    generate_transactions()