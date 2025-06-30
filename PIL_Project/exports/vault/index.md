# 🧭 Project Code Vault Index

This file is auto-generated. Use it as your starting dashboard in Obsidian.

---

## 📦 Modules
- [[builders.entity_graph_builder]]
- [[builders.linkage_builder]]
- [[builders.usage_map_builder]]
- [[builders.variable_usage_builder]]
- [[exporters.json_exporter]]
- [[exporters.markdown_vault_exporter]]
- [[exporters.md_exporter]]
- [[exporters.usage_map_exporter]]
- [[exporters.variable_usage_report_exporter]]
- [[exporters.vault_index_exporter]]
- [[loaders.asset_loader]]
- [[loaders.code_loader]]
- [[loaders.config_loader]]
- [[loaders.markdown_loader]]
- [[pipeline]]
- [[utils.docstring_utils]]
- [[utils.exceptions_reporter_utils]]
- [[utils.graph_utils]]
- [[utils.path_utils]]
- [[utils.snapshot_utils]]
- [[utils.test_coverage_utils]]
- [[validators.governance_validator]]

## 🏛️ Classs
- [[loaders.code_loader.ParentNodeVisitor]]

## ⚙️ Functions
- [[builders.entity_graph_builder.build_entity_graph]]
- [[builders.linkage_builder.extract_called_functions]]
- [[builders.linkage_builder.inject_call_links]]
- [[builders.usage_map_builder.build_usage_map]]
- [[builders.variable_usage_builder.build_variable_usage_map]]
- [[exporters.json_exporter.export_entity_graph]]
- [[exporters.markdown_vault_exporter._sanitize_filename]]
- [[exporters.markdown_vault_exporter.export_markdown_vault]]
- [[exporters.markdown_vault_exporter.friendly_name]]
- [[exporters.md_exporter.export_entity_markdown]]
- [[exporters.usage_map_exporter.export_usage_map]]
- [[exporters.variable_usage_report_exporter.export_variable_usage_markdown]]
- [[exporters.vault_index_exporter.export_vault_index]]
- [[loaders.asset_loader.export_path_list]]
- [[loaders.asset_loader.infer_tags_from_path]]
- [[loaders.asset_loader.load_asset_symbols]]
- [[loaders.code_loader.extract_nodes_from_ast]]
- [[loaders.code_loader.load_code_symbols]]
- [[loaders.config_loader.load_config]]
- [[loaders.markdown_loader.load_markdown_entries]]
- [[loaders.markdown_loader.parse_frontmatter]]
- [[pipeline.run_pipeline]]
- [[utils.docstring_utils.check_docstring_signature_match]]
- [[utils.docstring_utils.extract_docstring_metadata]]
- [[utils.exceptions_reporter_utils.generate_exception_report]]
- [[utils.graph_utils.walk_graph]]
- [[utils.path_utils.resolve_path]]
- [[utils.snapshot_utils.take_project_snapshot]]
- [[utils.test_coverage_utils.estimate_test_coverage]]
- [[validators.governance_validator.validate_governance_rules]]

## 🔹 Methods
- [[loaders.code_loader.visit]]

## 🧩 Variables
- [[loaders.asset_loader.SUPPORTED_EXTENSIONS]]
- [[loaders.markdown_loader.FRONTMATTER_RE]]
- [[utils.snapshot_utils.IGNORED_FOLDERS]]

---

## 📊 Live Dataview: All Non-Stable Code
```dataview
table type, status, tags
from "/home/runner/workspace/AdriftProject/PIL_Project/exports/vault"
where status != "stable"
sort type asc
```