"""Tests for Enterprise GraphRAG property-graph + vector lineage retrieval."""

from src.graphrag.lineage_engine import EnterpriseGraphRAGEngine


def test_graphrag_returns_human_oversight_lineage():
    engine = EnterpriseGraphRAGEngine()
    hits = engine.query_with_lineage("high-risk AI systems overseen by natural persons", top_k=1)
    assert len(hits) == 1
    assert hits[0].node_id == "eu-ai-act-art-14"
    assert any("human-in-the-loop" in p for p in hits[0].lineage_path)
    assert "MATCH (c:Clause" in hits[0].cypher_equivalent


def test_graphrag_returns_gdpr_pseudonymization_lineage():
    engine = EnterpriseGraphRAGEngine()
    hits = engine.query_with_lineage("data protection by design pseudonymization", top_k=1)
    assert hits[0].node_id == "gdpr-art-25"
    assert any("pii-redaction" in p for p in hits[0].lineage_path)
