# SQL Query Helper Agent - LangChain SQL Assistant Project

A beginner-friendly project that teaches you how to build a **single agent** using **LangChain + OpenAI**. The agent takes a plain English description of data you want and generates a SQL query, then explains what the query does line by line.

## What You'll Learn

- How LangChain works (LLMs, prompts, tools, agents)
- How to create tools using the `@tool` decorator
- How an agent decides which tools to call and in what order
- How `PromptTemplate` shapes LLM output
- How the agent's tool-calling loop works (think -> act -> observe -> repeat)
- How to generate SQL queries from natural language
- How to explain technical concepts (like SQL) in plain English

## How It Works

```
User's data request in plain English
       |
       v
  [Agent thinks: "I need to generate a SQL query first"]
       |
       v
  [Tool: generate_sql_query] --> creates a clean SQL SELECT query
       |
       v
  [Agent thinks: "Now I should explain this query"]
       |
       v
  [Tool: explain_sql_query] --> explains each clause in plain English
       |
       v
  SQL query + line-by-line explanation returned to user
```

## Prerequisites

- Python 3.10 or higher
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/NisargKadam/Langchain_sample_project.git
cd Langchain_sample_project
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Copy the example env file and add your real key:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your actual OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-key-here
```

## Run

```bash
python sql_query_helper_agent.py
```

You'll see an interactive prompt:

```
============================================================
  SQL QUERY HELPER AGENT
  Powered by LangChain + OpenAI
============================================================

Describe the data you want in plain English, and the agent will
generate a SQL query and explain it line by line.
```
Type 'quit' to exit.

Type your data request (e.g., "show me all customers who placed an order in the last 30 days") and the agent will handle the rest!

## Example

**Input:**
```
show me all customers who placed an order in the last 30 days
```

**Output:**
```
SQL Query:
SELECT c.customer_name, o.order_date
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);

Explanation:
- SELECT c.customer_name, o.order_date: Retrieves the customer's name and the date of their order.
- FROM customers c: Specifies the 'customers' table, giving it an alias 'c' for easier reference.
- JOIN orders o ON c.customer_id = o.customer_id: Joins the 'orders' table to link customers with their orders using the customer ID.
- WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY): Filters the results to only include orders placed within the last 30 days from today.
```

## Project Structure

```
.
├── sql_query_helper_agent.py   # Main agent code (fully commented)
├── requirements.txt     # Python dependencies
├── .env.example         # API key template
├── .gitignore           # Keeps secrets and venv out of git
└── README.md            # This file
```

## Tech Stack

- [LangChain](https://python.langchain.com/) - Framework for building LLM applications
- [OpenAI GPT-4o-mini](https://platform.openai.com/) - The LLM powering the agent
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management
