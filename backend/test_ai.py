from .ollama_client import ask_qwen
from .analytics import (
    get_merchant_analytics,
    get_anomaly_analysis,
)


analytics = get_merchant_analytics()
anomaly = get_anomaly_analysis()


prompt = f"""
You are an AI teammate helping a small merchant.

You have been given VERIFIED business data calculated by
the merchant's analytics system.

Do not invent numbers.
Do not calculate new financial figures yourself.
Use only the provided facts.

MERCHANT ANALYTICS:
{analytics}

ANOMALY ANALYSIS:
{anomaly}

Your task:

1. Explain what changed.
2. Identify the most important business problem.
3. Explain what you would investigate next.
4. Suggest practical actions.
5. Clearly separate facts from recommendations.

Keep the response concise and practical.
"""


print("\n===== AI TEAMMATE =====\n")

answer = ask_qwen(prompt)

print(answer)