# 🧭 Project Code Vault Index

This file is auto-generated. Use it as your starting dashboard in Obsidian.

---

## 📦 Modules
- [[pil_meta.builders.entity_graph_builder]]
- [[pil_meta.builders.linkage_builder]]
- [[pil_meta.builders.tag_and_link_applier_builders]]
- [[pil_meta.builders.usage_map_builder]]
- [[pil_meta.builders.variable_usage_builder]]
- [[pil_meta.exporters.json_exporter]]
- [[pil_meta.exporters.markdown_vault_exporter]]
- [[pil_meta.exporters.md_exporter]]
- [[pil_meta.exporters.variable_usage_report_exporter]]
- [[pil_meta.exporters.vault_index_exporter]]
- [[pil_meta.loaders.code_loader]]
- [[pil_meta.loaders.config_loader]]
- [[pil_meta.loaders.markdown_loader]]
- [[pil_meta.pipeline]]
- [[pil_meta.utils.docstring_utils]]
- [[pil_meta.utils.exceptions_reporter_utils]]
- [[pil_meta.utils.graph_utils]]
- [[pil_meta.utils.path_utils]]
- [[pil_meta.utils.test_coverage_utils]]
- [[pil_meta.validators.governance_validator]]
- [[scripts.rebuild_pil]]
- [[tests.test_pipeline]]

## 🏛️ Classs
- [[pil_meta.loaders.code_loader.ParentNodeVisitor]]

## ⚙️ Functions
- [[pil_meta.builders.entity_graph_builder.build_entity_graph]]
- [[pil_meta.builders.linkage_builder.extract_called_functions]]
- [[pil_meta.builders.linkage_builder.inject_call_links]]
- [[pil_meta.builders.tag_and_link_applier_builders.apply_tags_and_links]]
- [[pil_meta.builders.usage_map_builder.build_usage_map]]
- [[pil_meta.builders.variable_usage_builder.build_variable_usage_map]]
- [[pil_meta.exporters.json_exporter.export_entity_graph]]
- [[pil_meta.exporters.markdown_vault_exporter._sanitize_filename]]
- [[pil_meta.exporters.markdown_vault_exporter.export_markdown_vault]]
- [[pil_meta.exporters.markdown_vault_exporter.friendly_name]]
- [[pil_meta.exporters.md_exporter.export_to_markdown]]
- [[pil_meta.exporters.variable_usage_report_exporter.export_variable_usage_markdown]]
- [[pil_meta.exporters.vault_index_exporter.export_vault_index]]
- [[pil_meta.loaders.code_loader.extract_nodes_from_ast]]
- [[pil_meta.loaders.code_loader.load_code_symbols]]
- [[pil_meta.loaders.code_loader.module_name]]
- [[pil_meta.loaders.config_loader.load_config]]
- [[pil_meta.loaders.markdown_loader.load_markdown_entries]]
- [[pil_meta.pipeline.run_pipeline]]
- [[pil_meta.utils.docstring_utils.check_docstring_signature_match]]
- [[pil_meta.utils.docstring_utils.extract_docstring_metadata]]
- [[pil_meta.utils.exceptions_reporter_utils.generate_exception_report]]
- [[pil_meta.utils.graph_utils.walk_graph]]
- [[pil_meta.utils.path_utils.resolve_path]]
- [[pil_meta.utils.test_coverage_utils.estimate_test_coverage]]
- [[pil_meta.validators.governance_validator.validate_governance_rules]]
- [[tests.test_pipeline.test_pipeline_generates_valid_entity_graph]]

## 🔹 Methods
- [[pil_meta.loaders.code_loader.visit]]

---

## 📊 Live Dataview: All Non-Stable Code
```dataview
table type, status, tags
from "exports\vault"
where status != "stable"
sort type asc
```