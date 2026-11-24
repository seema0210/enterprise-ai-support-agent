
from langchain_core.tools import tool


@tool
def calculate_percentage(amount: float, percentage: float) -> float:
    """Calculate a percentage of a given amount."""

    return (amount * percentage) / 100

# The @tool decorator makes this Python function available as a tool that LangChain can describe to Qwen.