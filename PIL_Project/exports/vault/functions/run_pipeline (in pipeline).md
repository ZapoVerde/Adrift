# run_pipeline (in pipeline)
> **Fully qualified name:** `pipeline.run_pipeline`

**Type:** function
**Module:** 
**Status:** n/a
**Visibility:** n/a
**Tags:** 
**Deprecated:** ❌

---

## Description
Orchestrates the PIL metadata pipeline (scan + process + reporting).

## Full Docstring
```

```

## Links
- **calls**: utils.messaging_utils.print_run_context
- **calls**: utils.messaging_utils.print_folder_tree_summary
- **calls**: utils.messaging_utils.print_asset_scan_summary
- **calls**: utils.messaging_utils.print_symbol_extraction
- **calls**: utils.messaging_utils.print_entity_graph
- **calls**: utils.messaging_utils.print_exports
- **calls**: utils.messaging_utils.print_governance_summary
- **calls**: utils.messaging_utils.print_journal_entries_loaded
- **calls**: utils.messaging_utils.print_pipeline_complete
- **calls**: pipeline.PipelineResult
- **calls**: pipeline.run_pipeline
- **calls**: utils.messaging_utils.set_debug
- **calls**: loaders.config_loader.load_config
- **calls**: loaders.asset_loader.load_asset_symbols
- **calls**: builders.entity_graph_builder.build_entity_graph
- **calls**: builders.linkage_builder.inject_call_links
- **calls**: utils.export_cleanup_utils.clean_exports_dir
- **calls**: exporters.json_exporter.export_entity_graph
- **calls**: exporters.usage_map_exporter.export_usage_map
- **calls**: exporters.markdown_vault_exporter.export_markdown_vault
- **calls**: exporters.vault_index_exporter.export_vault_index
- **calls**: loaders.markdown_loader.load_markdown_entries
- **calls**: pipeline.print_full_report
- **calls**: builders.usage_map_builder.build_usage_map
- **calls**: utils.snapshot_utils.take_project_snapshot
- **calls**: loaders.code_loader.load_code_symbols


---
