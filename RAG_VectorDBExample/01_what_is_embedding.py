# ============================================================
#  SCRIPT 01 — What Is an Embedding?
#
#  This script answers the question:
#    "What does it actually mean to turn text into a vector?"
#
#  You will see:
#    - The raw numbers that represent a sentence
#    - How many dimensions OpenAI's model produces
#    - That similar sentences produce similar vectors
#    - Cosine similarity computed by hand
# ============================================================

import os
import sys
import math
sys.stdout.reconfigure(encoding="utf-8")
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EMBEDDING_MODEL = "text-embedding-ada-002"  # 1536 dimensions


# ── Helper: get one embedding vector ────────────────────────
def embed(text: str) -> list[float]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


# ── Helper: cosine similarity between two vectors ───────────
def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot   = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a ** 2 for a in vec_a))
    mag_b = math.sqrt(sum(b ** 2 for b in vec_b))
    return dot / (mag_a * mag_b)


# ── Step 1: Embed a sentence and inspect the raw vector ─────
print("=" * 60)
print("STEP 1 — Embedding a single sentence")
print("=" * 60)

sentence = "The cat sat on the mat."
vector = embed(sentence)

print(f"\nSentence : '{sentence}'")
print(f"Dimensions: {len(vector)}")          # 1536 dims with ada-002
print(f"\nFirst 10 values of the vector:")
for i, val in enumerate(vector[:10]):
    print(f"  [{i:4d}]  {val: .6f}")
print(f"  ...  (and {len(vector) - 10} more numbers)")


# ── Step 2: Compare similar vs different sentences ──────────
print("\n" + "=" * 60)
print("STEP 2 — Similarity: do similar sentences have similar vectors?")
print("=" * 60)

sentences = {
    "A": "I love eating pizza.",
    "B": "Pizza is my favourite food.",          # similar to A
    "C": "Rockets are launched into outer space.",  # very different
}

print("\nEmbedding three sentences — please wait...")
vectors = {key: embed(text) for key, text in sentences.items()}

pairs = [("A", "B"), ("A", "C"), ("B", "C")]

print()
for x, y in pairs:
    sim = cosine_similarity(vectors[x], vectors[y])
    bar = "#" * int(sim * 40)
    print(f"  Similarity({x} <-> {y}) = {sim:.4f}  {bar}")
    print(f"    {sentences[x][:55]}")
    print(f"    {sentences[y][:55]}")
    print()

print("Key insight:")
print("  Sentences A & B are about the same topic → HIGH similarity")
print("  Sentences A & C are completely different → LOW similarity")
print("  The model captures MEANING, not just keywords.")


# ── Step 3: Word analogy demo ───────────────────────────────
print("\n" + "=" * 60)
print("STEP 3 — Even single words become vectors")
print("=" * 60)

words = ["king", "queen", "man", "woman", "dog", "cat", "pizza"]
word_vectors = {w: embed(w) for w in words}

print()
for w1 in words[:5]:
    for w2 in words[:5]:
        if w1 >= w2:
            continue
        sim = cosine_similarity(word_vectors[w1], word_vectors[w2])
        print(f"  {w1:8s} <-> {w2:8s}  ->  {sim:.4f}")

print()
print("Notice that  king<->queen  and  man<->woman  score higher")
print("than  king<->pizza  -- the model understands relationships.")

print("\n✓ Script 01 complete. Run 02_store_in_vectordb.py next.")
