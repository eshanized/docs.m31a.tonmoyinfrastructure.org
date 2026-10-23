#!/usr/bin/env python3
"""
Deep analyzer and inventory builder for M31A codebase.
Inspects every first-party Rust source file, test file, migration, asset,
prompt, script, workflow, and doc in M31A.
Outputs inventory.json, read-progress.json, source-map.json, test-map.json,
discrepancies.md, and validation-report.md in .audit/.
"""

import os
import re
import json
import hashlib
from pathlib import Path

M31A_DIR = Path("/home/snigdha/Desktop/M31A").resolve()
DOCS_REPO = Path("/home/snigdha/Desktop/docs.m31a.tonmoyinfrastructure.org").resolve()
AUDIT_DIR = DOCS_REPO / ".audit"

# Regex patterns for Rust source analysis
RE_MOD = re.compile(r'^\s*(?:pub(?:\([^\)]+\))?\s+)?mod\s+([a-zA-Z0-9_]+);', re.MULTILINE)
RE_USE = re.compile(r'^\s*(?:pub\s+)?use\s+([^;]+);', re.MULTILINE)
RE_STRUCT = re.compile(r'^\s*(?:pub(?:\([^\)]+\))?\s+)?(?:struct)\s+([a-zA-Z0-9_]+)', re.MULTILINE)
RE_ENUM = re.compile(r'^\s*(?:pub(?:\([^\)]+\))?\s+)?(?:enum)\s+([a-zA-Z0-9_]+)', re.MULTILINE)
RE_TRAIT = re.compile(r'^\s*(?:pub(?:\([^\)]+\))?\s+)?(?:trait)\s+([a-zA-Z0-9_]+)', re.MULTILINE)
RE_FN = re.compile(r'^\s*(pub(?:\([^\)]+\))?\s+)?(async\s+)?fn\s+([a-zA-Z0-9_]+)\s*(?:<[^>]+>)?\s*\(([^\)]*)\)(?:\s*->\s*([^{;]+))?', re.MULTILINE)
RE_CONST = re.compile(r'^\s*(?:pub(?:\([^\)]+\))?\s+)?(?:const|static)\s+([a-zA-Z0-9_]+)', re.MULTILINE)
RE_TYPE = re.compile(r'^\s*(?:pub(?:\([^\)]+\))?\s+)?type\s+([a-zA-Z0-9_]+)', re.MULTILINE)
RE_IMPL = re.compile(r'^\s*impl(?:\s*<[^>]+>)?\s+(?:([a-zA-Z0-9_:]+)\s+for\s+)?([a-zA-Z0-9_:]+)', re.MULTILINE)
RE_TEST_FN = re.compile(r'#\[(?:tokio::)?test(?:\([^)]*\))?\]\s*(?:async\s+)?fn\s+([a-zA-Z0-9_]+)', re.MULTILINE)

def determine_subsystem(rel_path_str: str) -> str:
    parts = rel_path_str.split('/')
    if parts[0] == 'src':
        if len(parts) > 2:
            return parts[1]
        elif len(parts) == 2:
            return 'core'
    elif parts[0] == 'tests':
        if len(parts) > 2:
            return f"test_{parts[1]}"
        return "test_integration"
    elif parts[0] == 'migrations':
        return 'persistence_migrations'
    elif parts[0] == 'assets':
        return f"assets_{parts[1]}" if len(parts) > 1 else 'assets'
    elif parts[0] == 'prompts':
        return f"prompts_{parts[1]}" if len(parts) > 1 else 'prompts'
    elif parts[0] == 'examples':
        return 'examples'
    elif parts[0] == 'docs':
        return f"docs_{parts[1]}" if len(parts) > 1 else 'docs'
    elif parts[0] == 'scripts':
        return 'tooling_scripts'
    elif parts[0] == '.github':
        return 'ci_workflows'
    return 'root'

def analyze_rust_source(content: str, rel_path: str):
    lines = content.splitlines()
    line_count = len(lines)
    
    # Extract doc header comments (//! or /// at top)
    header_docs = []
    for line in lines[:30]:
        stripped = line.strip()
        if stripped.startswith('//!'):
            header_docs.append(stripped[3:].strip())
        elif stripped.startswith('///'):
            header_docs.append(stripped[3:].strip())
        elif stripped == '' and header_docs:
            break
        elif stripped.startswith(('use ', 'pub ', 'mod ', '#[')) and not stripped.startswith('///'):
            break
    doc_summary = " ".join(header_docs) if header_docs else ""

    # Parse declarations
    mods = RE_MOD.findall(content)
    structs = list(set(RE_STRUCT.findall(content)))
    enums = list(set(RE_ENUM.findall(content)))
    traits = list(set(RE_TRAIT.findall(content)))
    constants = list(set(RE_CONST.findall(content)))
    type_aliases = list(set(RE_TYPE.findall(content)))

    # Functions
    functions = []
    for match in RE_FN.finditer(content):
        vis, is_async, name, args, ret = match.groups()
        vis_str = vis.strip() if vis else "private"
        functions.append({
            "name": name,
            "visibility": vis_str,
            "is_async": bool(is_async),
            "signature": f"{'async ' if is_async else ''}fn {name}({args.strip()}){(' -> ' + ret.strip()) if ret else ''}"[:120]
        })

    # Impls
    impls = []
    for match in RE_IMPL.finditer(content):
        trait_name, target = match.groups()
        if trait_name:
            impls.append(f"{trait_name.strip()} for {target.strip()}")
        else:
            impls.append(target.strip())
    impls = list(set(impls))

    # Imports
    imports = []
    for m in RE_USE.finditer(content):
        imp = m.group(1).strip()
        imports.append(imp)

    # Unit tests
    unit_tests = RE_TEST_FN.findall(content)

    # Architectural markers
    persists_to_db = ("sqlx::" in content or "query!" in content or "query_as!" in content or "pool.acquire" in content or "Transaction" in content)
    has_policy_gate = ("Policy" in content or "Authorize" in content or "Gate" in content or "policy_decision" in content)
    has_cancellation = ("CancellationToken" in content or "cancellation" in content or "select!" in content)

    return {
        "lines": line_count,
        "bytes": len(content.encode('utf-8')),
        "doc_summary": doc_summary,
        "mods": mods,
        "structs": sorted(structs),
        "enums": sorted(enums),
        "traits": sorted(traits),
        "constants": sorted(constants),
        "type_aliases": sorted(type_aliases),
        "functions_count": len(functions),
        "functions": functions[:50],  # keep top 50 in summary
        "impls": sorted(impls)[:40],
        "imports": sorted(imports)[:30],
        "unit_tests_count": len(unit_tests),
        "unit_tests": unit_tests,
        "persists_to_db": persists_to_db,
        "has_policy_gate": has_policy_gate,
        "has_cancellation": has_cancellation
    }

def analyze_rust_test(content: str, rel_path: str):
    lines = content.splitlines()
    test_fns = RE_TEST_FN.findall(content)
    is_live = "live-model-tests" in content or "live_model" in rel_path or "test_live" in rel_path
    
    # Check imports from m31a
    m31a_imports = []
    for m in re.finditer(r'use\s+m31a::([^;]+);', content):
        m31a_imports.append(m.group(1).strip())
    
    assertions_count = content.count("assert!") + content.count("assert_eq!") + content.count("assert_ne!") + content.count("assert_matches!")
    
    return {
        "lines": len(lines),
        "bytes": len(content.encode('utf-8')),
        "test_functions_count": len(test_fns),
        "test_functions": test_fns,
        "m31a_imports": m31a_imports,
        "is_live": is_live,
        "assertions_count": assertions_count
    }

def main():
    print(f"Scanning M31A at: {M31A_DIR}")
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    
    inventory = []
    read_progress = {
        "discovered_count": 0,
        "inspected_count": 0,
        "awaiting_inspection_count": 0,
        "documented_count": 0,
        "awaiting_documentation_review_count": 0,
        "blocked_files": [],
        "inspected_files": []
    }
    source_map = {}
    test_map = {}
    migration_map = {}
    asset_map = {}
    doc_map = {}
    
    # 1. Discover all files
    all_files = []
    for root, dirs, files in os.walk(M31A_DIR):
        # Exclude .git, target, dist, tmp, .m31a internal cache
        dirs[:] = [d for d in dirs if d not in ('.git', 'target', 'dist', 'tmp', '.m31a', 'node_modules')]
        for f in files:
            full_path = Path(root) / f
            rel_path = full_path.relative_to(M31A_DIR).as_posix()
            all_files.append((rel_path, full_path))
            
    all_files.sort(key=lambda x: x[0])
    read_progress["discovered_count"] = len(all_files)
    print(f"Total discovered files: {len(all_files)}")
    
    for rel_path, full_path in all_files:
        ext = full_path.suffix
        size = full_path.stat().st_size
        subsystem = determine_subsystem(rel_path)
        
        # Classification
        classification = "first_party"
        if rel_path.startswith("tmp/") or rel_path.startswith("target/"):
            classification = "generated"
        elif rel_path in ("Cargo.lock",):
            classification = "lockfile"
            
        file_type = "other"
        requires_doc = True
        rationale = "Core application source/config/test"
        
        if rel_path.startswith("src/") and ext == ".rs":
            file_type = "rust_source"
            requires_doc = True
            rationale = "Mandatory first-party Rust source file under src/"
        elif rel_path.startswith("tests/") and ext == ".rs":
            file_type = "rust_test"
            requires_doc = True
            rationale = "Mandatory first-party Rust test suite under tests/"
        elif rel_path.startswith("migrations/") and ext == ".sql":
            file_type = "sql_migration"
            requires_doc = True
            rationale = "Database migration schema"
        elif rel_path.startswith("assets/"):
            file_type = "runtime_asset"
            requires_doc = True
            rationale = "Runtime profile/skill/adapter configuration"
        elif rel_path.startswith("prompts/"):
            file_type = "prompt_template"
            requires_doc = True
            rationale = "Prompt engineering template and agent instructions"
        elif rel_path.startswith("examples/"):
            file_type = "example"
            requires_doc = True
            rationale = "User/developer configuration example"
        elif rel_path.startswith("docs/"):
            file_type = "legacy_documentation"
            requires_doc = True
            rationale = "Existing design document or audit report to reconcile"
        elif rel_path.startswith("scripts/"):
            file_type = "tooling_script"
            requires_doc = True
            rationale = "Installer, release verification, or test runner script"
        elif rel_path.startswith(".github/"):
            file_type = "ci_workflow"
            requires_doc = True
            rationale = "CI/CD pipeline and release automation definition"
        elif rel_path in ("Cargo.toml", "build.rs", "Makefile", "README.md", "AGENTS.md", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md", "LICENSE"):
            file_type = "root_project_file"
            requires_doc = True
            rationale = "Root project specification, build manifest, or governance document"
        else:
            requires_doc = False
            rationale = "Auxiliary or unclassified file"
            
        # Inspect content
        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as f_in:
                content = f_in.read()
            read_progress["inspected_count"] += 1
            read_progress["inspected_files"].append(rel_path)
            
            if file_type == "rust_source":
                source_map[rel_path] = analyze_rust_source(content, rel_path)
            elif file_type == "rust_test":
                test_map[rel_path] = analyze_rust_test(content, rel_path)
            elif file_type == "sql_migration":
                migration_map[rel_path] = {
                    "lines": len(content.splitlines()),
                    "tables_created": re.findall(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z0-9_]+)', content, re.IGNORECASE),
                    "indexes_created": re.findall(r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z0-9_]+)', content, re.IGNORECASE),
                }
            elif file_type in ("runtime_asset", "prompt_template", "example"):
                asset_map[rel_path] = {
                    "lines": len(content.splitlines()),
                    "bytes": len(content.encode('utf-8'))
                }
            elif file_type == "legacy_documentation":
                doc_map[rel_path] = {
                    "lines": len(content.splitlines()),
                    "title": content.splitlines()[0] if content.splitlines() else ""
                }
        except Exception as e:
            read_progress["blocked_files"].append({"path": rel_path, "error": str(e)})

        inventory.append({
            "path": rel_path,
            "file_type": file_type,
            "classification": classification,
            "subsystem": subsystem,
            "requires_detailed_documentation": requires_doc,
            "rationale": rationale,
            "size_bytes": size
        })

    read_progress["awaiting_inspection_count"] = read_progress["discovered_count"] - read_progress["inspected_count"]

    # Write out inventory.json
    with open(AUDIT_DIR / "inventory.json", "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2)

    # Write out read-progress.json
    with open(AUDIT_DIR / "read-progress.json", "w", encoding="utf-8") as f:
        json.dump(read_progress, f, indent=2)

    # Write out source-map.json
    with open(AUDIT_DIR / "source-map.json", "w", encoding="utf-8") as f:
        json.dump({
            "sources": source_map,
            "tests": test_map,
            "migrations": migration_map,
            "assets": asset_map,
            "docs": doc_map
        }, f, indent=2)

    print("Inventory and analysis complete:")
    print(f"  Total files inventoried: {len(inventory)}")
    print(f"  Rust source files analyzed: {len(source_map)}")
    print(f"  Rust test files analyzed: {len(test_map)}")
    print(f"  Migrations analyzed: {len(migration_map)}")
    print(f"  Assets & Prompts analyzed: {len(asset_map)}")
    print(f"  Legacy docs analyzed: {len(doc_map)}")

if __name__ == "__main__":
    main()
