#!/usr/bin/env python3
"""Validate n8n workflow JSON files, docs, and catalog coverage."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple

try:
    import jsonschema
    _HAS_JSONSCHEMA = True
except ImportError:
    _HAS_JSONSCHEMA = False

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_EXT = ".json"
EXCLUDE_DIRS = {".git", ".github", "catalog", "schemas", "docs", "scripts", "__pycache__"}
EXCLUDE_FILES = {"package-lock.json"}

STATUS_VALUES = {"ready", "needs-configuration", "experimental", "not-tested", "deprecated"}

SUSPICIOUS_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{36,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN (?:RSA|EC|OPENSSH|PRIVATE) KEY-----"),
]

SAFE_PLACEHOLDER_TOKENS = {
    "OPENAI_API",
    "ANTHROPIC_API",
    "PINECONE_API",
    "COHERE_API",
    "HF_API",
    "SHEETS_API",
    "SHEET_ID",
    "SLACK_API",
    "SUPABASE_API",
    "REDIS_API",
    "WEAVIATE_API",
}


@dataclass
class Finding:
    level: str
    path: Path
    message: str


class Validator:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.errors: List[Finding] = []
        self.warnings: List[Finding] = []
        schema_path = self.repo_root / "schemas" / "workflow.schema.json"
        if schema_path.exists():
            try:
                self._schema = json.loads(schema_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self._schema = None
        else:
            self._schema = None

    def error(self, path: Path, message: str) -> None:
        self.errors.append(Finding("ERROR", path, message))

    def warn(self, path: Path, message: str) -> None:
        self.warnings.append(Finding("WARN", path, message))

    def discover_workflow_files(self) -> List[Path]:
        files: List[Path] = []
        for path in self.repo_root.rglob(f"*{WORKFLOW_EXT}"):
            rel = path.relative_to(self.repo_root)
            if any(part in EXCLUDE_DIRS for part in rel.parts):
                continue
            if rel.name in EXCLUDE_FILES:
                continue
            files.append(path)
        return sorted(files)

    def validate_workflow_file(self, path: Path) -> Dict[str, Any] | None:
        rel = path.relative_to(self.repo_root)
        try:
            raw = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            self.error(rel, f"File is not UTF-8 decodable: {exc}")
            return None

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            self.error(rel, f"Invalid JSON: {exc.msg} at line {exc.lineno} column {exc.colno}")
            return None

        if not isinstance(data, dict):
            self.error(rel, "Workflow file must be a JSON object")
            return None

        if _HAS_JSONSCHEMA and self._schema is not None:
            try:
                jsonschema.validate(data, self._schema)
            except jsonschema.ValidationError as exc:
                self.error(rel, f"Schema validation failed: {exc.message}")

        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            self.error(rel, "Missing or invalid `name` (expected non-empty string)")

        nodes = data.get("nodes")
        if not isinstance(nodes, list):
            self.error(rel, "Missing or invalid `nodes` (expected array)")
            nodes = []

        if "connections" not in data:
            self.warn(rel, "Missing `connections` (allowed, but uncommon for n8n workflows)")
            connections: Dict[str, Any] = {}
        else:
            connections = data.get("connections")
            if not isinstance(connections, dict):
                self.error(rel, "Invalid `connections` (expected object)")
                connections = {}

        seen_ids: Set[str] = set()
        name_set: Set[str] = set()
        for idx, node in enumerate(nodes):
            node_ref = f"node[{idx}]"
            if not isinstance(node, dict):
                self.error(rel, f"{node_ref}: node entry must be an object")
                continue

            node_id = node.get("id")
            if not isinstance(node_id, str) or not node_id.strip():
                self.error(rel, f"{node_ref}: missing/invalid node `id`")
            else:
                if node_id in seen_ids:
                    self.error(rel, f"{node_ref}: duplicate node id `{node_id}`")
                seen_ids.add(node_id)

            node_name = node.get("name")
            if isinstance(node_name, str) and node_name.strip():
                name_set.add(node_name)

            position = node.get("position")
            if not isinstance(position, list) or len(position) != 2 or not all(isinstance(v, (int, float)) for v in position):
                self.error(rel, f"{node_ref}: missing/invalid `position` (expected [x, y] numbers)")

            self._scan_for_suspicious_values(node, rel, context=node_ref)

        self._validate_connections(rel, connections, name_set)
        return data

    def _validate_connections(self, rel: Path, connections: Dict[str, Any], node_names: Set[str]) -> None:
        for source_name, edges_by_type in connections.items():
            if source_name not in node_names:
                self.warn(rel, f"Connection source `{source_name}` not found in node names")
            if not isinstance(edges_by_type, dict):
                self.error(rel, f"Connections for `{source_name}` must be an object")
                continue
            for edge_type, edge_groups in edges_by_type.items():
                if not isinstance(edge_groups, list):
                    self.error(rel, f"Connection `{source_name}.{edge_type}` must be an array")
                    continue
                for group in edge_groups:
                    if not isinstance(group, list):
                        self.error(rel, f"Connection group `{source_name}.{edge_type}` must be an array of edges")
                        continue
                    for edge in group:
                        if not isinstance(edge, dict):
                            self.error(rel, f"Connection edge in `{source_name}.{edge_type}` must be an object")
                            continue
                        target = edge.get("node")
                        if isinstance(target, str) and target and target not in node_names:
                            self.warn(rel, f"Connection target `{target}` not found in node names")

    def _scan_for_suspicious_values(self, value: Any, rel: Path, context: str) -> None:
        if isinstance(value, dict):
            for k, v in value.items():
                self._scan_for_suspicious_values(v, rel, f"{context}.{k}")
        elif isinstance(value, list):
            for i, v in enumerate(value):
                self._scan_for_suspicious_values(v, rel, f"{context}[{i}]")
        elif isinstance(value, str):
            if self._looks_like_placeholder_or_expression(value):
                return
            for pat in SUSPICIOUS_PATTERNS:
                if pat.search(value):
                    self.error(rel, f"Suspicious secret-like value detected at `{context}`")
                    break

    @staticmethod
    def _looks_like_placeholder_or_expression(value: str) -> bool:
        s = value.strip()
        if not s:
            return True
        if "{{" in s and "}}" in s:
            return True
        if s.startswith("="):
            return True
        if s in SAFE_PLACEHOLDER_TOKENS:
            return True
        if re.fullmatch(r"[A-Z][A-Z0-9_]{2,}", s):
            return True
        if "placeholder" in s.lower():
            return True
        return False

    def validate_catalog_and_docs(self, workflow_paths: Iterable[Path]) -> None:
        catalog_path = self.repo_root / "catalog" / "workflows.json"
        if not catalog_path.exists():
            self.error(catalog_path.relative_to(self.repo_root), "Missing catalog/workflows.json")
            return

        try:
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self.error(catalog_path.relative_to(self.repo_root), f"Invalid JSON: {exc.msg} at line {exc.lineno}")
            return

        entries = catalog.get("workflows")
        if not isinstance(entries, list):
            self.error(catalog_path.relative_to(self.repo_root), "`workflows` must be an array")
            return

        wf_set = {p.relative_to(self.repo_root).as_posix() for p in workflow_paths}
        seen_catalog_paths: Set[str] = set()

        for idx, entry in enumerate(entries):
            entry_ref = f"workflows[{idx}]"
            if not isinstance(entry, dict):
                self.error(catalog_path.relative_to(self.repo_root), f"{entry_ref} must be an object")
                continue

            rel_path = entry.get("relative_path")
            if not isinstance(rel_path, str) or not rel_path:
                self.error(catalog_path.relative_to(self.repo_root), f"{entry_ref} missing `relative_path`")
                continue
            seen_catalog_paths.add(rel_path)

            if rel_path not in wf_set:
                self.error(catalog_path.relative_to(self.repo_root), f"{entry_ref} references missing workflow `{rel_path}`")

            status = entry.get("status")
            if status not in STATUS_VALUES:
                self.error(catalog_path.relative_to(self.repo_root), f"{entry_ref} has invalid status `{status}`")

            doc_path = entry.get("documentation_path")
            if not isinstance(doc_path, str) or not doc_path:
                self.error(catalog_path.relative_to(self.repo_root), f"{entry_ref} missing `documentation_path`")
            else:
                full_doc = self.repo_root / doc_path
                if not full_doc.exists():
                    self.error(catalog_path.relative_to(self.repo_root), f"{entry_ref} documentation file missing: `{doc_path}`")

            providers = entry.get("providers")
            if providers is not None and not isinstance(providers, list):
                self.error(catalog_path.relative_to(self.repo_root), f"{entry_ref}.providers must be an array")

        missing = sorted(wf_set - seen_catalog_paths)
        for rel_path in missing:
            self.error(catalog_path.relative_to(self.repo_root), f"Workflow missing from catalog: `{rel_path}`")

        extra = sorted(seen_catalog_paths - wf_set)
        for rel_path in extra:
            self.error(catalog_path.relative_to(self.repo_root), f"Catalog contains non-existent workflow: `{rel_path}`")

    def print_findings(self) -> None:
        for finding in self.errors + self.warnings:
            print(f"[{finding.level}] {finding.path}: {finding.message}")
        print(f"\nValidation summary: {len(self.errors)} error(s), {len(self.warnings)} warning(s)")


def main() -> int:
    validator = Validator(REPO_ROOT)
    workflow_files = validator.discover_workflow_files()

    if not workflow_files:
        print("No workflow JSON files found.")
        return 1

    for wf in workflow_files:
        validator.validate_workflow_file(wf)

    validator.validate_catalog_and_docs(workflow_files)
    validator.print_findings()

    return 1 if validator.errors else 0


if __name__ == "__main__":
    sys.exit(main())
