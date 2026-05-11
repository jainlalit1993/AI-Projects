# LangChain Single-Agent Assignment

## Overview

You have been given a working LangChain agent project — **Email Humanizer** — as your reference implementation. Your task is to **build your own unique use case** using the exact same framework and patterns.

Study the `email_humanizer.py` file carefully. Your agent must follow the same structure:

```
[User Input] --> [Tool 1] --> [Tool 2] --> [Final Output]
```

---

## What You Must Build

Using the same LangChain patterns from the reference code:

- `ChatOpenAI` — the LLM
- `PromptTemplate` — to shape LLM responses
- `@tool` decorator — to define at least 2 tools
- `create_agent` — to wire everything together
- A `SYSTEM_PROMPT` — to define agent behaviour
- A `run_<your_agent>()` function — as the main entry point

---

## Submission Steps

1. **Fork or clone** this repo to your local machine
2. **Create your own Python file** (e.g., `recipe_generator.py`) — do NOT modify `email_humanizer.py`
3. **Build your use case** following the same structure
4. **Test it** — make sure it runs end-to-end with your OpenAI key
5. **Push your code** to a **new public GitHub repository** under your own account
6. **Share the GitHub link** in the Excel sheet shared on WhatsApp

Your repo must contain:
- Your agent `.py` file
- A `requirements.txt`
- A `.env.example` file (never commit your real `.env`)
- A `README.md` explaining what your agent does and how to run it

---

## Individual Assignments

---

### 1. Chan Wei Khjan — Resume Reviewer Agent

**Use Case:** A user pastes their resume text and a job description. The agent reviews the resume against the job requirements and suggests targeted improvements.

**Tool 1 — `analyze_resume_gaps`**
- Input: resume text + job description
- Task: Identify skills, keywords, and experience missing from the resume compared to the job description
- Output: A structured gap analysis

**Tool 2 — `suggest_resume_improvements`**
- Input: the gap analysis from Tool 1
- Task: Rewrite bullet points, suggest new sections, and recommend specific keywords to add
- Output: Concrete, actionable resume improvement suggestions

**System Prompt:** The agent acts as a professional resume coach helping candidates tailor their resume to a specific job posting.

---

### 2. Gurleen Kaur — Recipe Generator Agent

**Use Case:** A user provides a list of ingredients they have at home. The agent suggests a recipe and then produces step-by-step cooking instructions.

**Tool 1 — `suggest_recipe`**
- Input: comma-separated list of available ingredients
- Task: Suggest a suitable dish that can be made using those ingredients (may allow 1-2 common pantry staples)
- Output: Recipe name, description, and full ingredient list with quantities

**Tool 2 — `generate_cooking_steps`**
- Input: the recipe details from Tool 1
- Task: Convert the recipe into numbered, beginner-friendly cooking steps with timings
- Output: A clear step-by-step cooking guide

**System Prompt:** The agent acts as a friendly home chef who helps users cook meals with what they already have.

---

### 3. Komal Patil — Code Explainer Agent

**Use Case:** A user pastes a block of code (any language). The agent explains what it does in plain English and then adds inline comments to the code.

**Tool 1 — `explain_code`**
- Input: raw code snippet
- Task: Explain what the code does in simple, plain English — no jargon, suitable for a beginner
- Output: A paragraph-style plain English explanation

**Tool 2 — `add_inline_comments`**
- Input: the original code snippet
- Task: Rewrite the code with clear, helpful inline comments on every significant line
- Output: The fully commented version of the code

**System Prompt:** The agent acts as a patient coding tutor who makes any code understandable for beginners.

---

### 4. Anived Mishra — Story Writer Agent

**Use Case:** A user provides a theme or a one-line story prompt. The agent first creates a story outline and then expands it into a complete short story.

**Tool 1 — `create_story_outline`**
- Input: story theme or one-line prompt (e.g., "a robot who learns to feel emotions")
- Task: Generate a structured story outline with characters, setting, conflict, and resolution
- Output: A detailed story outline in bullet-point format

**Tool 2 — `write_short_story`**
- Input: the story outline from Tool 1
- Task: Expand the outline into a complete, engaging short story (400–600 words)
- Output: The full short story with a title

**System Prompt:** The agent acts as a creative fiction writer who can turn any idea into a compelling short story.

---

### 5. Amarnadh Ravipati — Customer Complaint Handler Agent

**Use Case:** A user (customer service rep) pastes a customer complaint. The agent classifies its severity and drafts a professional, empathetic response.

**Tool 1 — `classify_complaint`**
- Input: the customer complaint text
- Task: Classify the complaint by category (e.g., billing, product defect, delivery, service quality) and severity (Low / Medium / High / Critical)
- Output: Category, severity level, and a brief reason for the classification

**Tool 2 — `draft_complaint_response`**
- Input: the original complaint + classification from Tool 1
- Task: Write a professional, empathetic customer service response that acknowledges the issue, apologises, and offers a resolution path
- Output: A ready-to-send customer response

**System Prompt:** The agent acts as a senior customer service specialist who handles complaints with empathy and professionalism.

---

### 6. Lalit Jain — SQL Query Helper Agent

**Use Case:** A user describes what data they want in plain English. The agent generates a SQL query and then explains what the query does line by line.

**Tool 1 — `generate_sql_query`**
- Input: a plain English description of the data request (e.g., "show me all customers who placed an order in the last 30 days")
- Task: Write a clean, correct SQL SELECT query (assume standard table names like `customers`, `orders`, `products`)
- Output: A formatted SQL query

**Tool 2 — `explain_sql_query`**
- Input: the SQL query from Tool 1
- Task: Explain each clause of the query in plain English, line by line, so a non-technical person understands it
- Output: A line-by-line explanation of the query

**System Prompt:** The agent acts as a database assistant who bridges the gap between business users and SQL.

---

### 7. Gurkamal Singh — Product Description Writer Agent

**Use Case:** A user provides a product name and a list of features. The agent first writes a formal product description and then rewrites it as a catchy marketing copy.

**Tool 1 — `write_formal_description`**
- Input: product name and feature list
- Task: Write a structured, formal product description suitable for a product catalogue or documentation
- Output: A formal 150–200 word product description

**Tool 2 — `write_marketing_copy`**
- Input: the formal description from Tool 1
- Task: Transform the formal description into punchy, exciting marketing copy that sells the product emotionally
- Output: Engaging marketing copy with a headline, 2–3 short paragraphs, and a call-to-action

**System Prompt:** The agent acts as a product copywriter who can write both technical and marketing content.

---

### 8. Joseph — Meeting Notes Summarizer Agent

**Use Case:** A user pastes raw, messy meeting notes. The agent first creates a clean summary and then extracts all action items with owners and deadlines.

**Tool 1 — `summarize_meeting_notes`**
- Input: raw meeting notes (can be messy, bullet points, or stream-of-consciousness)
- Task: Extract and organise the key discussion points, decisions made, and topics covered into a clean summary
- Output: A structured meeting summary with sections for Attendees (if mentioned), Key Discussions, and Decisions Made

**Tool 2 — `extract_action_items`**
- Input: the raw meeting notes
- Task: Identify all action items, who is responsible, and deadlines mentioned (or mark as TBD if not stated)
- Output: A numbered list of action items in the format: `[Owner] — [Task] — [Deadline]`

**System Prompt:** The agent acts as an executive assistant who turns chaotic meeting notes into structured, actionable records.

---

### 9. Siddhesh Sawant — Travel Itinerary Planner Agent

**Use Case:** A user provides a destination and the number of days for their trip. The agent suggests top places to visit and then builds a day-by-day itinerary.

**Tool 1 — `suggest_places_to_visit`**
- Input: destination city/country and number of days
- Task: Suggest the top must-visit attractions, restaurants, and experiences, grouped by type (sightseeing, food, adventure, culture)
- Output: A categorised list of recommendations with a short description of each

**Tool 2 — `create_daily_itinerary`**
- Input: destination, number of days, and the suggestions from Tool 1
- Task: Organise the suggestions into a practical, time-efficient day-by-day itinerary (morning / afternoon / evening slots)
- Output: A complete travel itinerary, one section per day

**System Prompt:** The agent acts as a knowledgeable travel planner who creates personalised, realistic trip itineraries.

---

### 10. Karthik Balaje R — Interview Q&A Coach Agent

**Use Case:** A user provides a job role (e.g., "Data Analyst at a fintech startup"). The agent generates likely interview questions and then provides model answers.

**Tool 1 — `generate_interview_questions`**
- Input: job role and optionally a skill or domain to focus on
- Task: Generate 8–10 realistic interview questions covering technical skills, behavioural situations, and role-specific scenarios
- Output: A numbered list of interview questions grouped by type

**Tool 2 — `generate_model_answers`**
- Input: the list of questions from Tool 1 and the job role
- Task: Write concise, impressive model answers for each question using the STAR format (Situation, Task, Action, Result) where applicable
- Output: Each question followed by its model answer

**System Prompt:** The agent acts as a career coach who prepares candidates to ace job interviews with confidence.

---

### 11. Sai Sankar — Social Media Post Generator Agent

**Use Case:** A user provides a topic, product launch, or announcement. The agent first writes a formal press-style announcement and then converts it into an engaging social media post.

**Tool 1 — `write_formal_announcement`**
- Input: topic or announcement details (e.g., "launching our new AI-powered mobile app for fitness tracking")
- Task: Write a formal, professional announcement suitable for a company blog or press release
- Output: A structured formal announcement with a headline and 2–3 paragraphs

**Tool 2 — `convert_to_social_post`**
- Input: the formal announcement from Tool 1, plus the target platform (LinkedIn, Instagram, or Twitter/X)
- Task: Rewrite the announcement as an engaging social media post tailored to the chosen platform — use emojis, hashtags, and a hook opening line
- Output: A ready-to-post social media caption

**System Prompt:** The agent acts as a social media manager who can adapt formal content into platform-native posts.

---

### 12. Bala Krishna Yenumula — Bug Report Analyzer Agent

**Use Case:** A user pastes a bug report or error description. The agent identifies likely root causes and then suggests a structured debugging plan.

**Tool 1 — `identify_root_causes`**
- Input: bug report or error description (can include stack traces, error messages, or symptom descriptions)
- Task: Analyse the report and list the most likely root causes, ranked from most to least probable, with a brief reasoning for each
- Output: A ranked list of probable root causes

**Tool 2 — `suggest_debugging_steps`**
- Input: the bug description and the root cause analysis from Tool 1
- Task: Generate a step-by-step debugging plan — specific commands to run, logs to check, code areas to inspect
- Output: A numbered, actionable debugging checklist

**System Prompt:** The agent acts as a senior software engineer who helps developers debug issues systematically and efficiently.

---

### 13. Beadon Roy — Study Notes Generator Agent

**Use Case:** A user provides a topic they want to study (e.g., "how neural networks work"). The agent creates comprehensive study notes and then converts them into flashcard-style Q&A pairs.

**Tool 1 — `generate_study_notes`**
- Input: topic name and optionally a difficulty level (beginner / intermediate / advanced)
- Task: Write thorough, well-structured study notes covering key concepts, definitions, and examples
- Output: Study notes with clear headings, sub-points, and examples

**Tool 2 — `create_flashcards`**
- Input: the study notes from Tool 1
- Task: Convert the key concepts from the notes into 10–15 flashcard-style Q&A pairs for active recall practice
- Output: A numbered list of Q&A pairs in the format: `Q: [question] / A: [answer]`

**System Prompt:** The agent acts as a personal tutor who helps students learn any topic quickly through structured notes and revision flashcards.

---

### 14. Sagar Sable — Job Description Writer Agent

**Use Case:** A user provides a job title and key requirements. The agent drafts a formal job description and then rewrites it to be more engaging and attractive to candidates.

**Tool 1 — `draft_formal_jd`**
- Input: job title, required skills, experience level, and responsibilities
- Task: Write a complete, formal job description with sections for Role Overview, Responsibilities, Requirements, and What We Offer
- Output: A structured, formal job description

**Tool 2 — `make_jd_engaging`**
- Input: the formal JD from Tool 1
- Task: Rewrite the JD using inclusive, energetic language that excites candidates — remove corporate jargon, add personality, and highlight growth opportunities
- Output: A compelling, candidate-friendly job posting

**System Prompt:** The agent acts as a talent acquisition specialist who writes job descriptions that attract high-quality candidates.

## Evaluation Criteria

| Criteria | Points |
|---|---|
| Code follows the same LangChain agent structure as `email_humanizer.py` | 20 |
| Both tools are implemented correctly using `@tool` and `PromptTemplate` | 20 |
| Agent runs end-to-end without errors | 20 |
| `README.md` clearly explains the use case and how to run it | 20 |
| GitHub repo is public, clean, and has `.env.example` (no real API key committed) | 20 |
| **Total** | **100** |

---

## Tips

- Start by running the original `email_humanizer.py` first so you understand the flow
- Read `langchain_tutorial.md` included in this repo — it walks through every concept
- Your `.env` file must never be pushed to GitHub — add it to `.gitignore`
- Test with simple inputs first before trying complex ones
- The `SYSTEM_PROMPT` is the brain of your agent — write it clearly

---

*Deadline and submission link: shared on WhatsApp. Post your GitHub URL in the Excel sheet.*
