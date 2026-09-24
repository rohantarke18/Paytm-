from .actions import create_merchant_incident


result = create_merchant_incident(
    title="Payment failure spike detected",
    description=(
        "Recent failure rate increased significantly "
        "above the historical baseline. "
        "Merchant should investigate payment processing "
        "errors before taking further action."
    ),
    severity="high",
)

print("\n===== MERCHANT ACTION CREATED =====\n")

for key, value in result.items():
    print(f"{key}: {value}")