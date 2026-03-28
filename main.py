import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langchain_core.tools import tool

load_dotenv()

# ── Tools ──────────────────────────────────────────────────
@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    return "Error: Division by zero" if b == 0 else a / b

@tool
def power(base: float, exp: float) -> float:
    """Raise base to the power of exp."""
    return base ** exp

math_tools = [add, subtract, multiply, divide, power]

# ── Main ───────────────────────────────────────────────────
async def run_math_tutor(query: str):

    model = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

    # ✅ langgraph 1.1.3 uses "prompt" parameter
    calculator_agent = create_react_agent(
        model, math_tools, name="calculator_agent",
        prompt="Solve the math problem step by step using tools. Show all steps."
    )

    explainer_agent = create_react_agent(
        model, [], name="explainer_agent",
        prompt="Explain the math concept and why each step works. Keep it simple like explaining to a 15 year old."
    )

    quiz_agent = create_react_agent(
        model, [], name="quiz_agent",
        prompt="Generate exactly 2 similar practice problems. Do not solve them."
    )

    supervisor = create_supervisor(
        model=model,
        agents=[calculator_agent, explainer_agent, quiz_agent],
        prompt=(
            "You manage: calculator_agent, explainer_agent, quiz_agent.\n"
            "Order: calculator_agent → explainer_agent → quiz_agent.\n"
            "One agent at a time. Don't do work yourself.\n"
            "Final output sections: ✅ Solution | 📘 Explanation | 🧪 Practice Problems"
            "IMPORTANT: Use plain text only. No LaTeX. No \\( or \\) brackets ever."
        ),
        output_mode="last_message",
    ).compile()

    print(f"\n🚀 Math Tutor Started for: '{query}'\n")

    result = await supervisor.ainvoke({
        "messages": [{"role": "user", "content": query}]
    })

    print("\n" + "=" * 60)
    print("✅ FINAL TUTOR RESPONSE")
    print("=" * 60)
    print(clean_output(result["messages"][-1].content))

def clean_output(text: str) -> str:
    return text.replace("\\(", "").replace("\\)", "").replace("\\[", "").replace("\\]", "")
if __name__ == "__main__":
    query = "What is (15 * 4) + (100 / 5) - 2^3 ?"
    asyncio.run(run_math_tutor(query))