# 🚀 PostgreSQL Hybrid Search (Semantic + Full-Text + RRF)

A production-ready implementation of **Hybrid Search** combining:

* 🔍 PostgreSQL Full-Text Search (`tsvector`)
* 🧠 Semantic Search using `pgvector`
* ⚖️ Reciprocal Rank Fusion (RRF) for result merging

---

## 📌 Why Hybrid Search?

Traditional search fails in two ways:

| Problem                          | Example                                  |
| -------------------------------- | ---------------------------------------- |
| Keyword-only misses meaning      | "AI models" ≠ "machine learning systems" |
| Semantic-only misses exact terms | "PostgreSQL index" exact match needed    |

👉 **Hybrid Search solves both** by combining:

* **Lexical Search** → Exact keyword matching
* **Semantic Search** → Meaning-based similarity
* **RRF** → Smart ranking fusion

---

## 🏗️ Architecture

```text
User Query
    ↓
Embedding (OpenAI)
    ↓
 ┌───────────────┬───────────────┐
 │ Semantic Search │ Full-Text Search │
 │ (pgvector)     │ (tsvector)       │
 └───────────────┴───────────────┘
            ↓
     RRF Fusion Layer
            ↓
       Ranked Results
```

---

## 📂 Project Structure

```bash
postgres-hybrid-search-rrf/
│── app/
│   ├── db.py
│   ├── embeddings.py
│   ├── search.py
│   └── config.py
│
│── scripts/
│   └── setup.sql
│
│── main.py
│── requirements.txt
│── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Create Database

```bash
createdb hybrid_search
```

---

### 2️⃣ Enable Extensions & Tables

```bash
psql -d hybrid_search -f scripts/setup.sql
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set Environment Variable

```bash
export OPENAI_API_KEY=your_api_key
```

(Windows)

```bash
set OPENAI_API_KEY=your_api_key
```

---

### 5️⃣ Run the Project

```bash
python main.py
```

---

## 🔎 How It Works

### 1. Semantic Search

* Converts query → embedding
* Finds nearest vectors using:

```sql
embedding <=> query_embedding
```

---

### 2. Full-Text Search

* Uses PostgreSQL:

```sql
tsvector @@ plainto_tsquery
```

---

### 3. RRF (Reciprocal Rank Fusion)

Formula:

```text
score = α * semantic_rank + (1 - α) * lexical_rank
```

* `α = 0.5` → balanced search
* `α > 0.5` → more semantic
* `α < 0.5` → more keyword

---

## 🧠 Example

Query:

```text
"machine learning models"
```

Results:

* Finds documents with similar meaning
* Also prioritizes exact keyword matches
* Combines both into a ranked list

---

## 💡 Real Use Cases

### 🔹 1. RAG Systems (GenAI)

* ChatGPT-style document retrieval
* LangChain / LlamaIndex pipelines

### 🔹 2. Internal Knowledge Base

* Search across company docs
* HR, Legal, Tech docs

### 🔹 3. E-commerce Search

* "running shoes" ≈ "sports sneakers"
* Still match exact product names

### 🔹 4. Developer Docs Search

* Semantic understanding + exact APIs

---

## ⚡ Performance Tips

* Use **IVFFlat index** for large datasets
* Tune:

  ```sql
  lists = 100
  ```
* Run:

  ```sql
  ANALYZE documents;
  ```

---

## 🔧 Improvements (Next Steps)

* ✅ Add FastAPI REST API
* ✅ Add caching (Redis)
* ✅ Add reranking (Cross-Encoder)
* ✅ Switch to HNSW index
* ✅ Add pagination

---

## 🛑 Common Issues

### ❌ Slow Query

* Missing index → create IVFFlat + GIN

### ❌ No Results in Full-Text

* Ensure `tsvector` is populated

### ❌ Poor Semantic Results

* Use better embedding model

---

## 📌 Key Concepts

| Concept    | Description                            |
| ---------- | -------------------------------------- |
| pgvector   | Vector similarity search in PostgreSQL |
| tsvector   | Full-text search index                 |
| RRF        | Combines multiple ranking systems      |
| Embeddings | Numeric representation of text         |

---

## 🏁 Summary

This project gives you:

✅ Production-ready hybrid search
✅ Better relevance than standalone methods
✅ Foundation for GenAI + RAG systems

---

## ⭐ If you’re building:

* LLM apps
* Search engines
* AI assistants

👉 This is a **must-have pattern**

---

## 📬 License

MIT License
