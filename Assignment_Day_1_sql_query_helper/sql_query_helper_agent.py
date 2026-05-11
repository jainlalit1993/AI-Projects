"""
===========================================================================
 SQL QUERY HELPER AGENT -- A LangChain SQL Assistant Project
===========================================================================

 WHAT THIS PROJECT TEACHES YOU:
   1. How LangChain works (chains, prompts, LLMs, tools, agents)
   2. How to build a single agent that uses tools
   3. How to connect LangChain to OpenAI
   4. How prompt templates shape LLM output
   5. How an agent can generate SQL and explain it in plain English

 HOW LANGCHAIN WORKS (the big picture):
   LangChain is a framework that makes it easy to build LLM-powered apps.

     [User Input] --> [Prompt Template] --> [LLM (GPT)] --> [Output]

   - Prompt Template : A reusable template with placeholders (like a form)
   - LLM            : The AI model that generates text (OpenAI GPT)
   - Output         : The generated response

 WHAT IS AN AGENT?
   An agent is an LLM that can USE TOOLS and DECIDE what to do next.
   Unlike a simple chain (input -> LLM -> output), an agent can:
     1. Think about what it needs to do
     2. Pick a tool to use
     3. Use the tool and see the result
     4. Decide if it needs more steps or if it's done

   This is the tool-calling loop:
     THINK -> ACT -> OBSERVE -> THINK -> ... -> FINAL ANSWER

 HOW THIS PROJECT FLOWS:
   1. User describes the data they want in plain English.
   2. Agent calls generate_sql_query -> writes a clean SQL SELECT query.
   3. Agent calls explain_sql_query  -> explains the query line by line.
   4. Agent returns the SQL query and explanation to the user.

 KEY LANGCHAIN COMPONENTS USED:
   - ChatOpenAI      : LLM wrapper that sends prompts to OpenAI's GPT API
   - PromptTemplate  : Template with {placeholders} filled before sending to LLM
   - @tool decorator : Turns a Python function into a tool the agent can call
   - create_agent    : Wires LLM + tools + system prompt into a runnable agent

 SETUP:
   1. pip install -r requirements.txt
   2. Copy .env.example to .env and add your OpenAI API key
   3. python sql_query_helper_agent.py

 See langchain_tutorial.md for a full beginner's guide to LangChain.
"""

import logging
import sys
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("SQLQueryHelper")

logger.info("Starting SQL Query Helper Agent...")

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key.startswith("sk-your"):
    logger.error("OPENAI_API_KEY not set! Copy .env.example to .env and add your key.")
    sys.exit(1)

logger.info("API key loaded successfully")
logger.info("All LangChain components imported")
logger.info("Initializing the LLM (OpenAI GPT)...")

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7,
    verbose=True,
)

logger.info("LLM initialized: model=gpt-4.1-mini, temperature=0.7")
logger.info("Defining agent tools...")


@tool
def generate_sql_query(request: str) -> str:
    """
    Generates a SQL query based on a natural language description.
    Use this tool FIRST when the user provides a description of the data they want.
    Input should be the user's description of the desired data.
    Returns a structured SQL query.
    """
    logger.info(f"[Tool: generate_sql_query] Received request: '{request}'")

    draft_prompt = PromptTemplate(
        input_variables=["request"],
        template="""You are a professional SQL developer.
Given the following idea, write a structured SQL query.

Idea: {request}

Write the query with:
- A clear SELECT statement
- Proper column names
- Appropriate WHERE clauses if needed
- ORDER BY clause if needed
- sort the query in a readable format with line breaks and indentation
- basics of query optimization if applicable (e.g., using JOINs instead of subqueries, avoiding SELECT *, etc.)
- Support for JOINs if multiple tables are involved
- Support for GROUP BY if aggregation is needed
- Support to create stored procedures, functions etc if the query is complex, and provide the procedure code, along with the query that calls it.

Return ONLY the SQL query, nothing else.""",
    )

    formatted_prompt = draft_prompt.format(request=request)
    logger.info("[Tool: generate_sql_query] Sending prompt to LLM...")

    response = llm.invoke(formatted_prompt)

    logger.info("[Tool: generate_sql_query] Query generated successfully!")
    return response.content


@tool
def explain_sql_query(query: str) -> str:
    """
    Explains a SQL query in simple terms.
    Use this tool to understand what a SQL query does.
    Input should be the full SQL query text.
    Returns a human-readable explanation of the query.
    """
    logger.info("[Tool: explain_sql_query] Explaining the SQL query...")

    explain_prompt = PromptTemplate(
        input_variables=["query"],
        template="""You are an expert at explaining SQL queries in simple terms.

Explain what the SQL query does

Rules:
- Provide step by step explanation of the query
- Explain the purpose of each clause (SELECT, FROM, WHERE, etc.)
- Use simple language that a non-technical person can understand
- avoid technical jargon and focus on the intent of the query
- provide examples of what kind of data the query would return

SQL query:
{query}

Return the explanation, along with the query, in a clear and concise manner.""",
    )

    formatted_prompt = explain_prompt.format(query=query)
    logger.info("[Tool: explain_sql_query] Sending prompt to LLM...")

    response = llm.invoke(formatted_prompt)

    logger.info("[Tool: explain_sql_query] Query explained successfully!")
    return response.content


tools = [generate_sql_query, explain_sql_query]
logger.info(f"Tools registered: {[t.name for t in tools]}")
logger.info("Creating the agent...")

SYSTEM_PROMPT = """The agent acts as a database assistant who bridges the gap between business users and SQL.

You are a SQL Query Helper assistant. Your job is to help users
write and understand SQL queries based on their natural language descriptions.

When the user gives you a data fetch request, follow these steps:
1. First, use the generate_sql_query tool to create a structured SQL query.
2. Then, use the explain_sql_query tool to make the query understandable.
3. Return the final explained SQL query to the user along with the SQL query., BOTH are important.

Always use both tools in order: generate_sql_query, explain_sql_query."""

agent_graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    debug=True,
)

logger.info("Agent created and ready to run!")


def run_sql_query_helper(data_request: str) -> str:
    """
    Main function to run the SQL query helper agent.

    Args:
        data_request: A brief description of the data you want to fetch.
                      Example: get all customers who made a purchase in the last month

    Returns:
        A structured SQL query and its explanation.
    """

    logger.info("=" * 60)
    logger.info(f"USER'S DATA REQUEST: {data_request}")
    logger.info("=" * 60)
    logger.info("Agent is now thinking... watch the tool-calling loop below!")
    logger.info("-" * 60)

    result = agent_graph.invoke(
        {"messages": [HumanMessage(content=data_request)]}
    )

    final_query = result["messages"][-1].content

    logger.info("-" * 60)
    logger.info("Agent finished! Here's your structured SQL query and Explaination:")
    logger.info("=" * 60)

    return final_query


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  SQL QUERY HELPER AGENT")
    print("  Powered by LangChain + OpenAI")
    print("=" * 60)
    print("\nDescribe the data you want to fetch, and the agent will")
    print("create a structured SQL query for you with explanation.\n")
    print("Type 'quit' to exit.\n")

    while True:
        data_request = input("Your data request: ").strip()

        if not data_request:
            print("Please tell me what SQL assistance is needed, provide name of tables and columns if available.\n")
            continue

        if data_request.lower() in ("quit", "exit", "q"):
            print("\nGoodbye! See you next time!")
            break

        try:
            final_query = run_sql_query_helper(data_request)

            print("\n" + "=" * 60)
            print("YOUR STRUCTURED SQL QUERY AND EXPLANATION:")
            print("=" * 60)
            print(final_query)
            print("=" * 60 + "\n")

        except Exception as e:
            logger.error(f"Something went wrong: {e}")
            print(f"\nError: {e}")
            print("Please check your API key and try again.\n")
