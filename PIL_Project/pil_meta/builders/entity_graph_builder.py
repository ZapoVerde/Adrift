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
        graph[fqname] = {
            "fqname": fqname,
            "type": "function",
            "description": entry["description"],
            "tags": entry["tags"],
            "source_file": entry["source_file"],
            "test_coverage": entry["test_coverage"],
            "docstring_present": entry["docstring_present"],
            "linked_journal_entry": entry["linked_journal_entry"],
            "is_orphaned": entry["is_orphaned"],
            "metadata": entry,
            "links": entry["links"],
        }

    return graph
