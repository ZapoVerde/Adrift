# entity_graph_builder.py
"""
Wraps pre-enriched function records into graph nodes.

This builder assumes that the upstream loader (code_loader) has already
attached all required metadata, including tags, docstring status, and test
coverage placeholders.

Output format conforms to the `entity_graph.json` specification.
"""


def build_entity_graph(entities: list[dict]) -> dict:
    """
    Wrap each enriched entity into a compliant graph node.

    Parameters:
        entities (list[dict]): Raw or enriched entity records.

    Returns:
        dict: fqname → wrapped graph node
    """
    graph = {}

    for entry in entities:
        fqname = entry["fqname"]

        # ✅ Enforce deterministic, non-inferred linking
        links = [
            link for link in entry.get("links", [])
            if link["type"] in {"calls", "modifies", "linked_journal_entry"}
        ]

        graph[fqname] = {
            "fqname": fqname,
            "type": "function",
            "description": entry.get("description", ""),
            "tags": entry.get("tags", []),
            "source_file": entry.get("source_file", ""),
            "test_coverage": entry.get("test_coverage", None),
            "docstring_present": entry.get("docstring_present", False),
            "linked_journal_entry": entry.get("linked_journal_entry", None),
            "is_orphaned": entry.get("is_orphaned", False),
            "metadata": entry,
            "links": links,
        }
        # 🚫 Sanity check: no heuristic links allowed
        VALID_LINK_TYPES = {"calls", "modifies", "linked_journal_entry"}
        for node in graph.values():
            node["links"] = [
                link for link in node.get("links", [])
                if link["type"] in VALID_LINK_TYPES
            ]

    return graph
