# =============================================================================
# SQL Helper Graph -- A LangGraph Learning Project
# =============================================================================
#
# This project teaches you how LangGraph works by building a SQL helper
# assistant that provides personalized SQL assistance.
#
# WHAT THIS DOES:
# A user describes the data they need. The graph generates SQL and explains it.
# (e.g. "I want to see total sales by month for the last year")
#
# LANGGRAPH CONCEPTS COVERED:
# 1. State Management (Pydantic) -- user request flows through the graph
# 2. Nodes -- each function does one job (identify tables, generate SQL, check risks)
# 3. Sequential Execution -- nodes run in order, each building on the previous
# 4. Conditional Edges -- routing to simple vs advanced based on complexity
# 5. Graph Compilation -- turning the graph definition into a runnable app
#
# GRAPH STRUCTURE:
#
#   START
#     |
#   identify_tables
#     |
#   generate_sql_query
#     |
#   check_sql_risks
#     |
#   decide_complexity
#     |
#     (conditional)
#        /          \
#   simple?      advanced?
#     |               |
# simple_sql_response  advanced_sql_response
#     |               |
#    END             END
#
# HOW TO RUN:
#   python sql_helper_graph.py
#
# DEPENDENCIES (same as requirements.txt):
#   langgraph, langchain-openai, python-dotenv, pydantic
#
# =============================================================================

import sys
import operator
import json
from typing import Annotated

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()


class SQLHelperState(BaseModel):
    user_request: str = ""
    identified_tables: str = ""
    sql_query: str = ""
    risk_check: str = ""
    is_advanced: bool = False
    complexity_reason: str = ""
    final_response: str = ""
    messages: Annotated[list, operator.add] = []


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


def identify_tables(state: SQLHelperState) -> dict:
    response = llm.invoke(
        f"You are a database schema analyst. "
        f"A user wants: '{state.user_request}'. "
        f"Based on common database patterns, infer the most likely tables and fields needed. "
        f"List potential table names and their key fields. "
        f"Keep it concise, under 5 sentences."
    )
    return {
        "identified_tables": response.content,
        "messages": [f"[identify_tables] {response.content[:50]}..."]
    }


def generate_sql_query(state: SQLHelperState) -> dict:
    response = llm.invoke(
        f"You are a SQL query expert. "
        f"The user wants: '{state.user_request}'.\n\n"
        f"Identified tables/fields: {state.identified_tables}\n\n"
        f"Write a clean, correct SQL query that fulfills this request. "
        f"Use standard SQL syntax. Include appropriate WHERE clauses if needed. "
        f"Keep the query simple but complete."
    )
    return {
        "sql_query": response.content,
        "messages": [f"[generate_sql_query] Generated SQL query"]
    }


def check_sql_risks(state: SQLHelperState) -> dict:
    response = llm.invoke(
        f"You are a SQL security and performance auditor. "
        f"Review this SQL query for risks:\n\n{state.sql_query}\n\n"
        f"Check for: missing filters that could return too many rows, "
        f"missing joins, potential performance issues, security concerns. "
        f"Rate the query complexity as SIMPLE or ADVANCED. "
        f"Reply in JSON format: {{\"risks\": \"list any issues\", \"complexity\": \"SIMPLE/ADVANCED\"}}"
    )
    try:
        result = json.loads(response.content)
        risks = result.get("risks", "No major risks identified.")
        complexity = result.get("complexity", "SIMPLE")
    except (json.JSONDecodeError, KeyError):
        risks = "Could not parse risk check."
        complexity = "SIMPLE"

    return {
        "risk_check": risks,
        "messages": [f"[check_sql_risks] complexity={complexity}"]
    }


def decide_complexity(state: SQLHelperState) -> dict:
    # Simple decision based on risk check or query analysis
    # For now, assume if "ADVANCED" in risk_check, it's advanced
    is_advanced = "ADVANCED" in state.risk_check.upper()
    reason = "Based on query complexity analysis" if is_advanced else "Simple query detected"

    return {
        "is_advanced": is_advanced,
        "complexity_reason": reason,
        "messages": [f"[decide_complexity] advanced={is_advanced}"]
    }


def simple_sql_response(state: SQLHelperState) -> dict:
    response = llm.invoke(
        f"You are a helpful SQL assistant. "
        f"The user asked: '{state.user_request}'\n\n"
        f"Generated SQL:\n{state.sql_query}\n\n"
        f"Risk check: {state.risk_check}\n\n"
        f"Provide a simple explanation of the query and how to use it. "
        f"Keep it friendly and concise."
    )
    return {
        "final_response": f"SIMPLE SQL QUERY\n{'='*40}\n{state.sql_query}\n\nEXPLANATION:\n{response.content}",
        "messages": [f"[simple_sql_response] Generated simple response"]
    }


def advanced_sql_response(state: SQLHelperState) -> dict:
    response = llm.invoke(
        f"You are an expert SQL consultant. "
        f"The user asked: '{state.user_request}'\n\n"
        f"Generated SQL:\n{state.sql_query}\n\n"
        f"Risk check: {state.risk_check}\n\n"
        f"Provide a detailed explanation including: "
        f"1. What the query does step-by-step "
        f"2. Any potential optimizations "
        f"3. Alternative approaches if applicable "
        f"4. Usage warnings or considerations"
    )
    return {
        "final_response": f"ADVANCED SQL QUERY\n{'='*40}\n{state.sql_query}\n\nDETAILED ANALYSIS:\n{response.content}",
        "messages": [f"[advanced_sql_response] Generated advanced response"]
    }


def route_after_decision(state: SQLHelperState) -> str:
    if state.is_advanced:
        return "advanced"
    else:
        return "simple"


graph = StateGraph(SQLHelperState)

graph.add_node("identify_tables", identify_tables)
graph.add_node("generate_sql_query", generate_sql_query)
graph.add_node("check_sql_risks", check_sql_risks)
graph.add_node("decide_complexity", decide_complexity)
graph.add_node("simple_sql_response", simple_sql_response)
graph.add_node("advanced_sql_response", advanced_sql_response)

graph.add_edge(START, "identify_tables")

graph.add_edge("identify_tables", "generate_sql_query")
graph.add_edge("generate_sql_query", "check_sql_risks")
graph.add_edge("check_sql_risks", "decide_complexity")

graph.add_conditional_edges(
    "decide_complexity",
    route_after_decision,
    {
        "simple": "simple_sql_response",
        "advanced": "advanced_sql_response",
    }
)

graph.add_edge("simple_sql_response", END)
graph.add_edge("advanced_sql_response", END)

app = graph.compile()


def run_sql_helper(request: str):
    print("=" * 55)
    print("  SQL HELPER ASSISTANT")
    print(f"  You asked: \"{request}\"")
    print("=" * 55)

    result = app.invoke({
        "user_request": request,
        "messages": [],
    })

    print("\n" + "=" * 55)
    print("  YOUR SQL ASSISTANCE")
    print("=" * 55)
    print(f"\n{result['final_response']}")

    print("\n" + "-" * 55)
    print("  PROCESS LOG")
    print("-" * 55)
    for msg in result["messages"]:
        print(f"  {msg}")

    return result


if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  SQL HELPER ASSISTANT")
    print("=" * 55)
    print("\n  Describe the data you need and I'll generate")
    print("  SQL queries with explanations.")
    print("  Type 'quit' to exit.\n")

    while True:
        request = input("  What data do you need? > ").strip()

        if request.lower() in ("quit", "exit", "q"):
            print("\n  Happy querying! Goodbye!\n")
            break

        if not request:
            continue

        run_sql_helper(request)
        print("\n")
