# ============================================================
#  SCRIPT 02 — Storing Documents in a Vector Database
#
#  This script shows:
#    - How to embed multiple documents with OpenAI
#    - How to attach metadata to each document
#    - How ChromaDB stores: ID + vector + metadata + text
#    - Progress feedback so the class can see it working
# ============================================================

import os
import sys
import time
sys.stdout.reconfigure(encoding="utf-8")
import chromadb
from dotenv import load_dotenv
from openai import OpenAI

# Add the project root to the path so we can import data/
sys.path.append(os.path.dirname(__file__))
from data.sample_documents import DOCUMENTS

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-ada-002"
DB_PATH         = "./chroma_db"
COLLECTION_NAME = "rag_demo"

def embed(text: str) -> list[float]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


# ── Connect to (or create) a persistent ChromaDB ────────────
print("=" * 60)
print("STEP 1 — Connect to ChromaDB")
print("=" * 60)

db     = chromadb.PersistentClient(path=DB_PATH)
collection = db.get_or_create_collection(name=COLLECTION_NAME)

print(f"\n  Database path  : {os.path.abspath(DB_PATH)}")
print(f"  Collection     : {COLLECTION_NAME}")
print(f"  Documents already stored: {collection.count()}")

# Wipe the collection so we start fresh each run
if collection.count() > 0:
    db.delete_collection(COLLECTION_NAME)
    collection = db.get_or_create_collection(name=COLLECTION_NAME)
    print("  (Cleared existing data for a clean demo)")


# ── Embed every document and store it ───────────────────────
print("\n" + "=" * 60)
print("STEP 2 — Embed & store each document")
print("=" * 60)
print(f"\nTotal documents to store: {len(DOCUMENTS)}")
print()

ids        = []
embeddings = []
texts      = []
metadatas  = []

for i, doc in enumerate(DOCUMENTS, start=1):
    print(f"  [{i:02d}/{len(DOCUMENTS)}] Embedding: '{doc['metadata']['title']}'  ({doc['metadata']['category']})")

    vector = embed(doc["text"])

    ids.append(doc["id"])
    embeddings.append(vector)
    texts.append(doc["text"])
    metadatas.append(doc["metadata"])

    # Small pause so the API isn't hammered (also looks good in class!)
    time.sleep(0.2)

# ── Bulk-add everything to ChromaDB ─────────────────────────
collection.add(
    ids        = ids,
    embeddings = embeddings,
    documents  = texts,
    metadatas  = metadatas,
)

print(f"\n  ✓  Stored {collection.count()} documents in ChromaDB")


# ── Show what one stored record looks like ──────────────────
print("\n" + "=" * 60)
print("STEP 3 — What does one stored record look like?")
print("=" * 60)

sample = collection.get(
    ids     = ["space_001"],
    include = ["embeddings", "documents", "metadatas"],
)

print(f"\n  ID       : {sample['ids'][0]}")
print(f"  Text     : {sample['documents'][0][:80]}...")
print(f"\n  Metadata :")
for key, val in sample["metadatas"][0].items():
    print(f"    {key:10s}: {val}")
dims = len(sample['embeddings'][0])
print(f"\n  Embedding dimensions : {dims}")
print(f"  First 8 values       : {[round(v, 5) for v in sample['embeddings'][0][:8]]}")
print(f"\n  This is what ChromaDB stores for EVERY document:")
print("    ┌─────────────────────────────────────────────┐")
print("    │  ID       → unique identifier               │")
print("    │  vector   → 1536 float numbers              │")
print("    │  text     → original document text          │")
print("    │  metadata → category, title, source, year   │")
print("    └─────────────────────────────────────────────┘")

print("\n✓ Script 02 complete. Run 03_inspect_vectordb.py next.")
