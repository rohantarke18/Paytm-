from .tools import get_recent_failure_analysis


result = get_recent_failure_analysis()

print("\n===== RECENT FAILURE ANALYSIS =====\n")

for key, value in result.items():
    print(f"{key}: {value}")