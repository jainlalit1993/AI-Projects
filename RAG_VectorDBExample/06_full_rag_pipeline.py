# ============================================================
#  SCRIPT 06 — Full RAG Pipeline
#
#  Putting it all together:
#    Retrieve relevant chunks from the vector DB
#    → inject them into a GPT prompt
#    → get a grounded answer
#
#  The "hallucination demo" section asks a question both
#  WITH and WITHOUT retrieval so students can see the
#  difference a vector DB makes.
# ============================================================

import os
import sys
sys.stdout.reconfigure(encoding="utf-8")
import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-ada-002"
CHAT_MODEL      = "gpt-4.1-mini"
DB_PATH         = "./chroma_db"
COLLECTION_NAME = "rag_demo"
TOP_K           = 3

def embed(text: str) -> list[float]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def safe_input(prompt: str) -> str:
    """Read input when running interactively; skip cleanly otherwise."""
    if not sys.stdin or not sys.stdin.isatty():
        return ""
    try:
        return input(prompt)
    except EOFError:
        return ""


def retrieve(question: str, k: int = TOP_K) -> list[dict]:
    """Return top-k relevant chunks from the vector DB."""
    db         = chromadb.PersistentClient(path=DB_PATH)
    collection = db.get_or_create_collection(name=COLLECTION_NAME)

    q_vector = embed(question)
    results  = collection.query(
        query_embeddings = [q_vector],
        n_results        = k,
        include          = ["documents", "metadatas", "distances"],
    )

    chunks = []
    for doc_id, text, meta, dist in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "id":       doc_id,
            "text":     text,
            "metadata": meta,
            "distance": dist,
        })
    return chunks


def ask_without_rag(question: str) -> str:
    """Ask GPT with no extra context (baseline / potential hallucination)."""
    response = client.chat.completions.create(
        model    = CHAT_MODEL,
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",   "content": question},
        ],
        max_tokens  = 200,
        temperature = 0.7,
    )
    return response.choices[0].message.content.strip()


def ask_with_rag(question: str, chunks: list[dict]) -> str:
    """Ask GPT with retrieved context injected into the prompt."""
    context_block = "\n\n".join(
        f"[Source: {c['metadata']['title']} — {c['metadata']['source']}, {c['metadata']['year']}]\n{c['text']}"
        for c in chunks
    )
    system_prompt = (
        "You are a helpful assistant. Answer the user's question using ONLY "
        "the context provided below. If the context doesn't contain enough "
        "information, say so. Do not make things up.\n\n"
        f"CONTEXT:\n{context_block}"
    )
    response = client.chat.completions.create(
        model    = CHAT_MODEL,
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": question},
        ],
        max_tokens  = 300,
        temperature = 0.2,   # low temp for factual grounded answers
    )
    return response.choices[0].message.content.strip()


# ── Full pipeline demo ───────────────────────────────────────
def run_rag_demo(question: str) -> None:
    print("\n" + "=" * 60)
    print(f"QUESTION: {question}")
    print("=" * 60)

    # ── 1. Retrieve ─────────────────────────────────────────
    print("\n── Step 1: Retrieve relevant chunks ────────────────────")
    chunks = retrieve(question)
    for i, c in enumerate(chunks, 1):
        sim = round(1 / (1 + c["distance"]), 4)
        print(f"\n  [{i}] {c['metadata']['title']}  (similarity: {sim})")
        print(f"       {c['text'][:100]}...")

    # ── 2. Build the prompt ─────────────────────────────────
    print("\n── Step 2: Retrieved chunks are injected into the prompt ─")
    print("  The chunks above become part of the system message.")
    print("  GPT can only answer using what we give it.")

    # ── 3. Answer WITHOUT RAG ───────────────────────────────
    print("\n── Step 3: Answer WITHOUT RAG (no context) ─────────────")
    answer_no_rag = ask_without_rag(question)
    print(f"\n  {answer_no_rag}")

    # ── 4. Answer WITH RAG ──────────────────────────────────
    print("\n── Step 4: Answer WITH RAG (grounded in our docs) ───────")
    answer_rag = ask_with_rag(question, chunks)
    print(f"\n  {answer_rag}")

    print("\n  ┌─────────────────────────────────────────────────────┐")
    print("  │  WITHOUT RAG → GPT uses general training knowledge   │")
    print("  │  WITH RAG    → GPT is constrained to our documents   │")
    print("  │  RAG = more accurate, traceable, updatable answers   │")
    print("  └─────────────────────────────────────────────────────┘")


# ── Main ─────────────────────────────────────────────────────
print("=" * 60)
print("FULL RAG PIPELINE DEMO")
print("=" * 60)
print("\nThis demo shows the complete RAG flow:")
print("  User question → embed → retrieve → inject → GPT answer")
print("\nWe will compare answers WITH and WITHOUT retrieval.\n")

DEMO_QUESTIONS = [
    "How fast can cheetahs run and how is that possible?",
    "What happens inside a quantum computer?",
    "Why is fermentation used in cooking and food preservation?",
]

for q in DEMO_QUESTIONS:
    run_rag_demo(q)
    safe_input("\n  [Press Enter to continue to the next question...]\n")


# ── Interactive mode ─────────────────────────────────────────
print("=" * 60)
print("ASK YOUR OWN QUESTION")
print("=" * 60)
print("(Type 'quit' to exit)\n")

while True:
    user_q = safe_input("Your question: ").strip()
    if user_q.lower() in ("quit", "exit", "q", ""):
        break
    run_rag_demo(user_q)

print("\n✓ Demo complete! You have seen the full RAG pipeline.")
print("  Embed → Store → Retrieve → Ground → Answer")
