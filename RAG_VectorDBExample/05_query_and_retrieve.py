# ============================================================
#  SCRIPT 05 — Querying the Vector Database
#
#  This script shows exactly how retrieval works:
#    1. Your question is embedded into a vector
#    2. ChromaDB compares it to every stored vector
#    3. The closest matches (by cosine distance) are returned
#    4. You can see the distance scores and metadata
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
DB_PATH         = "./chroma_db"
COLLECTION_NAME = "rag_demo"
TOP_K           = 3

def embed(text: str) -> list[float]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


# ── Connect ─────────────────────────────────────────────────
db         = chromadb.PersistentClient(path=DB_PATH)
collection = db.get_or_create_collection(name=COLLECTION_NAME)


# ── Demo queries ─────────────────────────────────────────────
DEMO_QUERIES = [
    "How do rockets travel to other planets?",
    "What makes bees so important for nature?",
    "How does bread rise when baking?",
    "What is a neural network?",
    "Which animals live in the coldest places on Earth?",
]


def run_query(question: str) -> None:
    print("\n" + "=" * 60)
    print(f"QUERY: {question}")
    print("=" * 60)

    # Step 1 — embed the query
    print("\nStep 1 — Embedding the query...")
    q_vector = embed(question)
    print(f"  Query vector: [{q_vector[0]:.5f}, {q_vector[1]:.5f}, "
          f"{q_vector[2]:.5f}, ... ] ({len(q_vector)} dims)")

    # Step 2 — search ChromaDB
    print(f"\nStep 2 — Searching for top {TOP_K} nearest neighbours...")
    results = collection.query(
        query_embeddings = [q_vector],
        n_results        = TOP_K,
        include          = ["documents", "metadatas", "distances"],
    )

    doc_ids   = results["ids"][0]
    distances = results["distances"][0]    # lower = more similar
    metas     = results["metadatas"][0]
    docs      = results["documents"][0]

    # ChromaDB returns L2 distance by default.
    # Convert to a 0-1 similarity score for readability.
    # similarity ≈ 1 / (1 + distance) for an intuitive display
    similarities = [1 / (1 + d) for d in distances]

    # Step 3 — display results
    print(f"\nStep 3 — Results ranked by similarity:\n")

    for rank, (doc_id, dist, sim, meta, text) in enumerate(
        zip(doc_ids, distances, similarities, metas, docs), start=1
    ):
        bar = "█" * int(sim * 30)
        print(f"  Rank #{rank}  ──────────────────────────────────────")
        print(f"    ID          : {doc_id}")
        print(f"    Title       : {meta['title']}")
        print(f"    Category    : {meta['category']}")
        print(f"    Source      : {meta['source']}  ({meta['year']})")
        print(f"    Distance    : {dist:.6f}  (lower = closer)")
        print(f"    Similarity  : {sim:.4f}  {bar}")
        print(f"    Text snippet: {text[:110]}...")
        print()

    print("  → ChromaDB found these by measuring the distance between")
    print("    the query vector and every stored document vector.")
    print("    No keyword matching — pure geometric proximity!")


# ── Run all demo queries ─────────────────────────────────────
print("=" * 60)
print("VECTOR DB QUERY DEMO")
print("=" * 60)
print(f"\nDatabase has {collection.count()} documents.")
print(f"Retrieving top {TOP_K} results for each query.\n")

for q in DEMO_QUERIES:
    run_query(q)

# ── Interactive mode ─────────────────────────────────────────
print("\n" + "=" * 60)
print("TRY YOUR OWN QUERY")
print("=" * 60)
print("(Type 'quit' to exit)\n")

while True:
    user_q = input("Your question: ").strip()
    if user_q.lower() in ("quit", "exit", "q", ""):
        break
    run_query(user_q)

print("\n✓ Script 05 complete. Run 06_full_rag_pipeline.py next.")
