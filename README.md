# Enterprise GraphRAG with Regulatory Citation Lineage

<p align="left">
  <img src="https://img.shields.io/badge/GraphRAG-NetworkX%20%2B%20Neo4j%20Cypher-10B981?style=flat-square" alt="GraphRAG">
  <img src="https://img.shields.io/badge/Compliance-EU%20AI%20Act%20%7C%20GDPR-8B5CF6?style=flat-square" alt="EU AI Act & GDPR">
  <img src="https://img.shields.io/badge/Provenance-Multi--Hop%20Lineage-0EA5E9?style=flat-square" alt="Lineage">
  <img src="https://img.shields.io/badge/CI-Ruff%20%7C%20Bandit%20%7C%20Pytest-F59E0B?style=flat-square" alt="CI">
</p>

A **Hybrid Property-Graph + Vector Retrieval (GraphRAG)** engine combining **NetworkX** graph traversal, **Neo4j Cypher** query generation, and vector similarity over European regulatory texts (**EU AI Act 2024/1689** & **GDPR**) to produce **verifiable, multi-hop technical control lineage**.

---

## Table of Contents
- [Why GraphRAG for Regulatory Lineage?](#why-graphrag-for-regulatory-lineage)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage Example](#usage-example)
- [License](#license)

---

## Why GraphRAG for Regulatory Lineage?

Flat chunk-based RAG retrieves isolated paragraphs without preserving the structural relationships between **legal obligations** (e.g., *EU AI Act Article 14*) and **engineering controls** (e.g., *human-in-the-loop escalation gates*). GraphRAG bridges vector retrieval with property-graph traversal so every answer carries an auditable provenance path.

---

## Architecture

```
Compliance Query ("high-risk AI human oversight")
                     │
                     ▼
       ┌───────────────────────────┐
       │   Vector Similarity Rank  │ ──▶ Matches Clause Nodes (Art. 12, 14, GDPR 25)
       └───────────────────────────┘
                     │
                     ▼
       ┌───────────────────────────┐
       │  Property-Graph Traversal │ ──▶ Expands [:REQUIRES_CONTROL] Edges
       │   (NetworkX / Neo4j)      │
       └───────────────────────────┘
                     │
                     ▼
       LineageHit(
         lineage_path = ["EU AI Act (2024/1689) Article 14 -> human-in-the-loop"],
         cypher_equivalent = "MATCH (c:Clause ...)-[:REQUIRES_CONTROL]->(ctrl)"
       )
```

---

## Quick Start

```bash
git clone https://github.com/FirdowsRahaman/enterprise-graphrag-lineage.git
cd enterprise-graphrag-lineage
pip install -r requirements.txt
PYTHONPATH=. pytest tests -v
```

---

## Usage Example

```python
from src.graphrag.lineage_engine import EnterpriseGraphRAGEngine

engine = EnterpriseGraphRAGEngine()
hits = engine.query_with_lineage("data protection by design pseudonymization", top_k=1)
print(hits[0].lineage_path)
print(hits[0].cypher_equivalent)
```

---

## License
This project is licensed under the MIT License.
