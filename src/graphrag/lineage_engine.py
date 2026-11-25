"""Hybrid Property-Graph + Vector Retrieval with Verifiable Citation Lineage."""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

import networkx as nx


@dataclass(frozen=True)
class RegulatoryClause:
    """Node in the regulatory knowledge graph."""

    node_id: str
    regulation: str
    article: str
    text: str
    controls: tuple[str, ...]


@dataclass(frozen=True)
class LineageHit:
    """Retrieved regulatory node with multi-hop provenance lineage."""

    node_id: str
    regulation: str
    article: str
    text: str
    score: float
    lineage_path: list[str]
    cypher_equivalent: str


REGULATORY_NODES: tuple[RegulatoryClause, ...] = (
    RegulatoryClause(
        node_id="eu-ai-act-art-12",
        regulation="EU AI Act (2024/1689)",
        article="Article 12",
        text="High-risk AI systems shall allow automatic recording of events (logs) over the system lifetime.",
        controls=("immutable-audit-log", "otel-traceability"),
    ),
    RegulatoryClause(
        node_id="eu-ai-act-art-14",
        regulation="EU AI Act (2024/1689)",
        article="Article 14",
        text="High-risk AI systems shall be designed so they can be effectively overseen by natural persons.",
        controls=("human-in-the-loop", "escalation-gate"),
    ),
    RegulatoryClause(
        node_id="gdpr-art-25",
        regulation="GDPR (2016/679)",
        article="Article 25",
        text="Controllers shall implement data protection by design and by default, including pseudonymization.",
        controls=("pii-redaction", "zero-egress-vpc"),
    ),
)


def _tokens(text: str) -> Counter[str]:
    return Counter(re.findall(r"[a-z0-9]+", text.lower()))


def _cosine(a: Counter[str], b: Counter[str]) -> float:
    common = set(a) & set(b)
    num = sum(a[k] * b[k] for k in common)
    denom = math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values()))
    return num / denom if denom > 0 else 0.0


class EnterpriseGraphRAGEngine:
    """Builds a NetworkX property graph of regulations -> controls and executes hybrid retrieval."""

    def __init__(self) -> None:
        self.graph = nx.DiGraph()
        self._vectors: dict[str, Counter[str]] = {}
        for clause in REGULATORY_NODES:
            self.graph.add_node(
                clause.node_id,
                kind="Clause",
                regulation=clause.regulation,
                article=clause.article,
                text=clause.text,
            )
            self._vectors[clause.node_id] = _tokens(f"{clause.regulation} {clause.article} {clause.text}")
            for ctrl in clause.controls:
                self.graph.add_node(ctrl, kind="TechnicalControl")
                self.graph.add_edge(clause.node_id, ctrl, relation="REQUIRES_CONTROL")

    def query_with_lineage(self, query: str, top_k: int = 2) -> list[LineageHit]:
        """Rank clauses by vector similarity and expand 1-hop technical control lineage."""
        q_vec = _tokens(query)
        scored = [
            (node_id, _cosine(q_vec, vec))
            for node_id, vec in self._vectors.items()
        ]
        ranked = sorted(scored, key=lambda x: x[1], reverse=True)[:top_k]

        hits: list[LineageHit] = []
        for node_id, score in ranked:
            attrs = self.graph.nodes[node_id]
            controls = list(self.graph.successors(node_id))
            lineage = [f"{attrs['regulation']} {attrs['article']} -> {ctrl}" for ctrl in controls]
            cypher = (
                f"MATCH (c:Clause {{id: '{node_id}'}})-[:REQUIRES_CONTROL]->(ctrl:TechnicalControl) "
                "RETURN c.article, ctrl.id"
            )
            hits.append(
                LineageHit(
                    node_id=node_id,
                    regulation=attrs["regulation"],
                    article=attrs["article"],
                    text=attrs["text"],
                    score=round(score, 4),
                    lineage_path=lineage,
                    cypher_equivalent=cypher,
                )
            )
        return hits
