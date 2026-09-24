import json
import re

from backend.analytics import (
    get_merchant_analytics,
    get_anomaly_analysis,
)

from backend.tools import (
    get_recent_failure_analysis,
)

from backend.ollama_client import ask_qwen


def extract_tool_request(text):
    """
    Extract a JSON tool request from the model response.

    Expected format:

    {
        "tool": "get_recent_failure_analysis"
    }
    """

    match = re.search(
        r'\{.*?"tool".*?\}',
        text,
        re.DOTALL
    )

    if not match:
        return None

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def run_agent():

    print("\n🤖 Merchant AI Teammate starting...\n")

    # --------------------------------------------------
    # STEP 1 — Collect verified business facts
    # --------------------------------------------------

    analytics = get_merchant_analytics()
    anomaly = get_anomaly_analysis()

    print("📊 Merchant data collected.")

    # --------------------------------------------------
    # STEP 2 — Ask Qwen what information it needs
    # --------------------------------------------------

    investigation_prompt = f"""
You are an autonomous AI teammate for a merchant.

Your job is to investigate business problems using
verified data and available tools.

Do NOT invent numbers.

VERIFIED MERCHANT ANALYTICS:

{json.dumps(analytics, indent=2)}

VERIFIED ANOMALY ANALYSIS:

{json.dumps(anomaly, indent=2)}

AVAILABLE TOOL:

get_recent_failure_analysis

This tool returns:
- recent transaction count
- recent failed transaction count
- recent failure rate
- failed transaction value
- recent failure reasons

You should decide whether this tool is necessary.

If you need the tool, your response MUST contain this JSON:

{{"tool": "get_recent_failure_analysis"}}

Do not invent tool results.

If the tool is not needed, respond with:

{{"tool": null}}

Keep your response short.
"""

    decision = ask_qwen(investigation_prompt)

    print("\n===== AI TOOL DECISION =====\n")
    print(decision)

    # --------------------------------------------------
    # STEP 3 — Detect requested tool
    # --------------------------------------------------

    tool_request = extract_tool_request(decision)

    if not tool_request:
        print("\n⚠️ No valid tool request detected.")
        return

    tool_name = tool_request.get("tool")

    # --------------------------------------------------
    # STEP 4 — Execute the requested tool
    # --------------------------------------------------

    if tool_name == "get_recent_failure_analysis":

        print("\n🔧 Executing tool: get_recent_failure_analysis()")

        tool_result = get_recent_failure_analysis()

        print("\n📊 Tool result:")
        print(json.dumps(tool_result, indent=2))

    else:

        print(f"\n⚠️ Unknown tool requested: {tool_name}")
        return

    # --------------------------------------------------
    # STEP 5 — Give tool result back to Qwen
    # --------------------------------------------------

    final_prompt = f"""
You are an autonomous AI teammate for a merchant.

You previously identified a business anomaly.

Here are the VERIFIED overall analytics:

{json.dumps(analytics, indent=2)}

Here is the VERIFIED anomaly analysis:

{json.dumps(anomaly, indent=2)}

You requested this tool:

get_recent_failure_analysis()

The tool returned the following VERIFIED data:

{json.dumps(tool_result, indent=2)}

Now produce the final investigation.

Your response must contain:

1. What happened
2. Evidence from the data
3. Most likely root cause
4. What should be investigated next
5. Recommended merchant action

IMPORTANT:

- Use only numbers provided by the system.
- Do not invent numbers.
- Clearly distinguish evidence from inference.
- Do not claim that an external payment gateway is down unless the data proves it.
- Keep the response practical.
"""

    final_answer = ask_qwen(final_prompt)

    print("\n===== FINAL AI INVESTIGATION =====\n")
    print(final_answer)


if __name__ == "__main__":
    run_agent()