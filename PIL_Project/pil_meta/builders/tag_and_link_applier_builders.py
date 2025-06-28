# tag_and_link_applier_builders.py
"""
Graph Enrichment: Tags and Semantic Links (builders)

Populates known tags and journal links into the graph based on
explicit mappings (not heuristics or inference).
"""

def apply_tags_and_links(graph: dict) -> dict:
    """
    Attach known tags and semantic links to specific nodes in the graph.

    Parameters:
        graph (dict): Entity graph keyed by fully qualified name (fqname)

    Returns:
        dict: The enriched graph with added tags and semantic links
    """
    # Manual mappings — expand this as systems evolve
    manual_tags = {
        "pil_meta.pipeline.run_pipeline": ["pipeline", "entrypoint"],
        "pil_meta.builders.entity_graph_builder.build_entity_graph": ["builder", "graph"],
        "pil_meta.builders.linkage_builder.inject_call_links": ["builder", "linkage"],
        "pil_meta.exporters.json_exporter.export_entity_graph": ["exporter", "json"],
        "pil_meta.loaders.code_loader.load_code_symbols": ["loader", "code"]
    }

    journal_links = {
        "pil_meta.pipeline.run_pipeline": {
            "target": "PIL Metadata Strategy",
            "type": "inferred_journal_link",
            "confidence": 1.0
        }
    }

    for fqname, node in graph.items():
        # Add tags if known
        if fqname in manual_tags:
            node["tags"] = manual_tags[fqname]

        # Add journal link if known
        if fqname in journal_links:
            node.setdefault("links", []).append(journal_links[fqname])

    return graph
