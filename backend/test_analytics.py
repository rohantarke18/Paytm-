from .analytics import (
    get_merchant_analytics,
    get_anomaly_analysis,
)


print("\n===== MERCHANT ANALYTICS =====")

analytics = get_merchant_analytics()

for key, value in analytics.items():
    print(f"{key}: {value}")


print("\n===== ANOMALY ANALYSIS =====")

anomaly = get_anomaly_analysis()

for key, value in anomaly.items():
    print(f"{key}: {value}")