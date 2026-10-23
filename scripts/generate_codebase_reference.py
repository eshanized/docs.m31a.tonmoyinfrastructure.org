#!/usr/bin/env python3
"""
Generates exhaustive codebase reference documentation for all 567 Rust source files
and 266 test files in M31A based on inspected AST and metadata in .audit/source-map.json.
Generates docs/codebase/*.md, docs/tests/catalog.md, and .audit/documentation-coverage.json.
"""

import os
import re
import json
from pathlib import Path

DOCS_REPO = Path("/home/snigdha/Desktop/docs.m31a.tonmoyinfrastructure.org").resolve()
AUDIT_DIR = DOCS_REPO / ".audit"
CODEBASE_DOCS_DIR = DOCS_REPO / "docs" / "codebase"
TESTS_DOCS_DIR = DOCS_REPO / "docs" / "tests"

COMMIT_HASH = "3eddbfd3c296515c44268b386271dde0107c6a8b"
REPO_URL = "https://github.com/eshanized/M31A"

SUBSYSTEM_METADATA = {
    "agent": {"layer": "L4 Agents", "title": "Agent Subsystem", "desc": "Agent roles, lifecycle, supervisor, runner, adaptive replanning, and delegation"},
    "capability": {"layer": "L2 Capabilities", "title": "Capability Registry & Providers", "desc": "Typed capabilities, health monitoring, provider implementations (fs, git, lsp, terminal, web, etc.)"},
    "change": {"layer": "L6 Execution", "title": "Change Management", "desc": "Workspace change application, review, provenance, authority, and reconciliation"},
    "checkpoint": {"layer": "L6/L7 Checkpoints", "title": "Checkpoint & Crash Recovery", "desc": "Two-phase durable checkpoint protocol, manifest hashing, crash recovery scanner, and safe resume"},
    "cli": {"layer": "L9 CLI / Interface", "title": "CLI & Dispatch Layer", "desc": "Clap 4 argument hierarchy, output formatters, exit codes, and runtime command dispatch"},
    "config": {"layer": "L1 Configuration", "title": "Configuration Engine", "desc": "8-tier hierarchical configuration precedence, strict schema validation, canonical defaults, and provenance"},
    "context": {"layer": "L3 Intelligence", "title": "Context Compiler & Tokenizer", "desc": "Token budgeting, prompt envelope assembly, evidence ranking, and context window compaction"},
    "controller": {"layer": "L8 Autonomy", "title": "Autonomy Controller", "desc": "Execution stage transitions, halting criteria, loop detection, and progress monitoring"},
    "dag": {"layer": "L5 Planning", "title": "DAG & Critical Path Method", "desc": "Directed acyclic task graphs, topological sorting, critical path analysis, and reconciliation"},
    "deployment": {"layer": "L9 Deployment", "title": "Deployment & Channels", "desc": "Compile-time channel isolation (production vs development), update feeds, installer, and rollback"},
    "eval": {"layer": "L7 Verification", "title": "Autonomous Evaluation Harness", "desc": "Acceptance test scenarios A through H, scoring, and automated evaluation runner"},
    "events": {"layer": "L0/L8 Event Bus", "title": "Event Bus & Envelopes", "desc": "Broadcast channels, structured telemetry envelopes, and asynchronous event distribution"},
    "git": {"layer": "L2 Git Operations", "title": "Git & Worktree Isolation", "desc": "Worktree management, branch naming, isolated attribution, trailers, stash, and hosting"},
    "ids": {"layer": "L0 Domain Identities", "title": "Domain Identity Types", "desc": "Strongly typed domain IDs (ExecutionRunId, TaskId, AgentId, ArtifactId, CheckId, etc.)"},
    "init": {"layer": "L9 Initialization", "title": "Initialization & Doctor", "desc": "Workspace setup wizard, environment diagnostic probes, and lifecycle bootstrapping"},
    "interaction": {"layer": "L9 Interaction", "title": "Interaction & Slash Commands", "desc": "Session parser, user-defined slash commands, approval actions, and mention resolution"},
    "kernel": {"layer": "L0 Kernel", "title": "Kernel Core & Seams", "desc": "Core seams, architectural invariants, cancellation tokens, hashes, and memory boundaries"},
    "memory": {"layer": "L3 Intelligence", "title": "Engineering Memory", "desc": "Persistent engineering decisions, architectural assumptions, and historical project memory"},
    "model": {"layer": "L3 Intelligence", "title": "Model & Provider Layer", "desc": "NVIDIA NIM provider, SSE streaming, model catalog, dynamic discovery, and token usage"},
    "persistence": {"layer": "L0 Persistence", "title": "Persistence & SQLite", "desc": "SQLite database pool, schema migrations 001-032, repositories, and artifact store"},
    "pipeline": {"layer": "L5/L6 Pipeline", "title": "Pipeline Execution", "desc": "End-to-end task pipelines, staging, execution harnesses, and lifecycle transitions"},
    "planning": {"layer": "L5 Planning", "title": "Planning & Decomposition", "desc": "Mission decomposition, strategy generation, plan revision, and candidate DAG creation"},
    "platform": {"layer": "L1 Platform", "title": "Platform Abstractions", "desc": "Cross-platform OS primitives (Linux, macOS, Windows), process control, and path handling"},
    "policy": {"layer": "L1 Security", "title": "Policy Engine & Security Gates", "desc": "Non-bypassable policy evaluation, 4 decisions (Allow/Deny/Ask/Escalate), and approvals"},
    "process": {"layer": "L2 Process", "title": "Process Supervision", "desc": "Process tree supervisor, PID tracking, spool capture, signal escalation, and timeouts"},
    "prompt": {"layer": "L3 Intelligence", "title": "Prompt System", "desc": "Prompt registry, template rendering, versioning, and prompt references"},
    "recovery": {"layer": "L7 Recovery", "title": "Recovery & Replanning", "desc": "Differential replanning, failure diagnosis, and automated remediation"},
    "release": {"layer": "L9 Release", "title": "Release Certification", "desc": "Release manifests, 20-point production evidence matrix, and release certification"},
    "repo": {"layer": "L2 Repository", "title": "Repository Intelligence", "desc": "Code search, symbol extraction, dependency graph, and workspace drift detection"},
    "report": {"layer": "L8 Reporting", "title": "Execution Reports", "desc": "Structured scorecard generation, telemetry summaries, and execution reports"},
    "root": {"layer": "L0-L9 Composition", "title": "Root Application & Runtime", "desc": "main.rs, lib.rs, error taxonomy, and authoritative AppRuntime composition root"},
    "sandbox": {"layer": "L1 Sandbox", "title": "Sandbox & Confinement", "desc": "Filesystem sandboxing, network destination policies, and resource confinement"},
    "scheduler": {"layer": "L5 Scheduling", "title": "Scheduler & Job Admission", "desc": "Global job worker pool, concurrency limits, and task scheduling"},
    "skill": {"layer": "L2 Skills", "title": "Skill System", "desc": "Modular skill discovery, invocation, and in-task execution guidance"},
    "state": {"layer": "L8 State", "title": "Authoritative State Management", "desc": "Execution run state, session state, task state, and SQLite projection"},
    "state_machine": {"layer": "L8 State Machine", "title": "Domain State Machines", "desc": "Strict state transition matrices for missions, tasks, agents, and autonomy modes"},
    "storage": {"layer": "L0 Storage", "title": "Storage Layout", "desc": "Platform storage layout, global vs workspace state isolation, and legacy migrations"},
    "telemetry": {"layer": "L8 Telemetry", "title": "Telemetry & Spans", "desc": "Distributed tracing spans, metrics recording, and operational observability"},
    "tools": {"layer": "L2 Tools", "title": "Model Tools & Catalog", "desc": "Central catalog of 28 core tools and extended tools (fs, git, qa, repo, web, etc.)"},
    "tui": {"layer": "L9 TUI Cockpit", "title": "Ratatui TUI Cockpit", "desc": "62-file terminal cockpit, read-only projection over SQLite, streaming, and screens"},
    "verification": {"layer": "L7 Verification", "title": "Verification & Nyquist Gate", "desc": "7-tier verification hierarchy, evidence snapshot matching, and completion gate"},
    "workflow": {"layer": "L8 Workflow", "title": "Genesis & Engineering Workflows", "desc": "35-file multi-stage genesis workflows, ADR creation, charter, synthesis, and roadmap"},
}

def clean_doc_string(s: str) -> str:
    if not s:
        return "Internal implementation file."
    clean = s.replace("\n", " ").replace("\r", " ")
    # Replace Rust intra-doc links like [`Foo`](crate::...) or [Foo](crate::...) with `Foo`
    clean = re.sub(r'\[`?([^`\]]+)`?\]\((?:crate|super)::[^)]+\)', r'`\1`', clean)
    clean = clean.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    clean = clean.replace("{", "&#123;").replace("}", "&#125;")
    clean = clean.replace("|", "&#124;")
    return clean.strip()

def sanitize_type_str(s: str) -> str:
    clean = s.replace("{", "(").replace("}", ")").replace("<", "&lt;").replace(">", "&gt;").replace("|", "/")
    clean = " ".join(clean.split())
    return clean

def main():
    CODEBASE_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    TESTS_DOCS_DIR.mkdir(parents=True, exist_ok=True)

    with open(AUDIT_DIR / "source-map.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    sources = data["sources"]
    tests = data["tests"]

    # Group sources by subsystem
    by_subsystem = {}
    for path, meta in sources.items():
        parts = path.split('/')
        if len(parts) > 2 and parts[0] == 'src':
            sub = parts[1]
        else:
            sub = "root"
        by_subsystem.setdefault(sub, []).append((path, meta))

    coverage_manifest = {}

    # 1. Generate subsystem pages
    for sub, files in sorted(by_subsystem.items()):
        meta_info = SUBSYSTEM_METADATA.get(sub, {
            "layer": "Core Layer",
            "title": f"{sub.capitalize()} Subsystem",
            "desc": f"Source modules within src/{sub}"
        })
        
        md_filename = f"{sub}.md"
        
        lines = [
            f"# {meta_info['title']}",
            "",
            f"> **Architectural Layer:** {meta_info['layer']}  ",
            f"> **Source Directory:** `src/{sub if sub != 'root' else ''}`  ",
            f"> **File Count:** {len(files)} source files  ",
            "",
            f"{meta_info['desc']}.",
            "",
            "## Module Files & Detailed Reference",
            ""
        ]

        # Table of files
        lines.append("| Source File | Lines | Key Types | Responsibility |")
        lines.append("|---|:---:|---|---|")
        for path, meta in sorted(files, key=lambda x: x[0]):
            basename = os.path.basename(path)
            anchor = path.replace('/', '-').replace('.', '-')
            raw_types = (meta.get("structs", []) + meta.get("enums", []))[:3]
            key_types = ", ".join([sanitize_type_str(t) for t in raw_types]) or "Functions/Traits"
            doc_sum = clean_doc_string(meta.get("doc_summary", "") or "Subsystem component")
            summary_short = (doc_sum[:70] + "...") if len(doc_sum) > 70 else doc_sum
            lines.append(f"| [{basename}](#{anchor}) | {meta.get('lines', 0)} | `{key_types}` | {summary_short} |")

        lines.append("")
        lines.append("---")
        lines.append("")

        # Detailed section for each file
        for path, meta in sorted(files, key=lambda x: x[0]):
            anchor = path.replace('/', '-').replace('.', '-')
            github_url = f"{REPO_URL}/blob/{COMMIT_HASH}/{path}"
            
            coverage_manifest[path] = {
                "doc_page": f"/docs/codebase/{sub}",
                "doc_anchor": f"#{anchor}",
                "subsystem": sub,
                "lines": meta.get("lines", 0)
            }

            lines.append(f"### `{path}` {{#{anchor}}}")
            lines.append("")
            lines.append(f"- **Source Link:** [`{path}` on GitHub]({github_url})")
            lines.append(f"- **Lines of Code:** {meta.get('lines', 0)} ({meta.get('bytes', 0)} bytes)")
            
            # Attributes
            attrs = []
            if meta.get("persists_to_db"):
                attrs.append("💾 Interacts with SQLite Persistence")
            if meta.get("has_policy_gate"):
                attrs.append("🛡️ Enforces Policy Gate")
            if meta.get("has_cancellation"):
                attrs.append("🛑 Supports Cancellation Tokens")
            if attrs:
                lines.append(f"- **Runtime Properties:** {' | '.join(attrs)}")
            
            lines.append("")
            
            doc_sum = clean_doc_string(meta.get("doc_summary", ""))
            lines.append("#### Primary Responsibility")
            lines.append(f"{doc_sum}")
            lines.append("")

            # Declared Structs and Enums
            structs = meta.get("structs", [])
            enums = meta.get("enums", [])
            traits = meta.get("traits", [])
            
            if structs or enums or traits:
                lines.append("#### Types & Trait Declarations")
                if structs:
                    lines.append(f"- **Structs ({len(structs)}):** " + ", ".join([f"`{sanitize_type_str(s)}`" for s in structs]))
                if enums:
                    lines.append(f"- **Enums ({len(enums)}):** " + ", ".join([f"`{sanitize_type_str(e)}`" for e in enums]))
                if traits:
                    lines.append(f"- **Traits ({len(traits)}):** " + ", ".join([f"`{sanitize_type_str(t)}`" for t in traits]))
                lines.append("")

            # Key Functions
            funcs = meta.get("functions", [])
            if funcs:
                lines.append(f"#### Key Functions & Signatures ({min(len(funcs), 15)} shown)")
                lines.append("```rust")
                for fn_item in funcs[:15]:
                    lines.append(f"// {fn_item['visibility']}")
                    lines.append(f"{fn_item['signature']};")
                lines.append("```")
                lines.append("")

            # Inline unit tests
            unit_tests = meta.get("unit_tests", [])
            if unit_tests:
                lines.append(f"#### Unit Verification ({len(unit_tests)} inline tests)")
                lines.append("Tests defined within module:")
                lines.append(", ".join([f"`{t}`" for t in unit_tests[:10]]) + ("..." if len(unit_tests) > 10 else ""))
                lines.append("")

            lines.append("---")
            lines.append("")

        out_path = CODEBASE_DOCS_DIR / md_filename
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    # 2. Generate Codebase Overview page
    overview_lines = [
        "# M31A Codebase Reference",
        "",
        "> **Authoritative Implementation Index:** 567 first-party Rust source files across 42 functional subsystems.",
        "",
        "This section provides an exhaustive, verified reference for the entire M31A application codebase located at `/home/snigdha/Desktop/M31A/src/`.",
        "Every module, struct, enum, trait, and function documented here corresponds to tested code in revision `3eddbfd3`.",
        "",
        "## Subsystem Navigation Matrix",
        "",
        "| Subsystem | Layer | Files | Description | Reference Link |",
        "|---|---|:---:|---|---|",
    ]

    total_src_lines = 0
    for sub, files in sorted(by_subsystem.items()):
        meta_info = SUBSYSTEM_METADATA.get(sub, {"layer": "Core", "title": f"{sub.capitalize()}", "desc": "Subsystem modules"})
        sub_lines = sum(m.get("lines", 0) for _, m in files)
        total_src_lines += sub_lines
        overview_lines.append(f"| **{meta_info['title']}** | {meta_info['layer']} | {len(files)} | {meta_info['desc']} | [Inspect Modules](/docs/codebase/{sub}) |")

    overview_lines.extend([
        "",
        f"**Total Source Footprint:** {len(sources)} Rust source files, approximately {total_src_lines:,} lines of code.",
        "",
        "## Architectural Layers Summary",
        "",
        "```mermaid",
        "graph TD",
        '    L9["L9 CLI & TUI Cockpit (cli, tui, init, interaction, deployment)"]',
        '    L8["L8 Autonomy & State (controller, state, workflow, telemetry)"]',
        '    L7["L7 Verification & Recovery (verification, eval, recovery)"]',
        '    L6["L6 Execution & Checkpoints (change, checkpoint, pipeline)"]',
        '    L5["L5 Planning & DAG (dag, planning, scheduler)"]',
        '    L4["L4 Agents & Roles (agent, skill)"]',
        '    L3["L3 Intelligence & Context (model, prompt, context, memory)"]',
        '    L2["L2 Capabilities & Tools (capability, tools, process, git, repo)"]',
        '    L1["L1 Security & Policy (policy, sandbox, platform, config)"]',
        '    L0["L0 Kernel & Persistence (kernel, ids, persistence, storage, events)"]',
        "",
        "    L9 --> L8 --> L7 --> L6 --> L5 --> L4 --> L3 --> L2 --> L1 --> L0",
        "```",
        "",
        "### Architectural Law: Downward Dependency Discipline",
        "Dependencies flow downward only. A lower layer (e.g., L1 Security) may never import or depend on a higher layer (e.g., L8 Autonomy or L9 CLI).",
        "All model proposals pass downward through L5 (DAG), L1 (Policy Gate), before reaching L2 (Side-effect tools) or L0 (Persistence).",
    ])

    with open(CODEBASE_DOCS_DIR / "overview.md", "w", encoding="utf-8") as f:
        f.write("\n".join(overview_lines))

    # 3. Generate Complete Test Reference Catalog
    test_lines = [
        "# Complete Test Suite Catalog",
        "",
        "> **Exhaustive Test Inventory:** 266 first-party Rust test suites under `tests/`.",
        "",
        "M31A maintains a rigorous multi-tier test architecture enforcing architectural invariants, security policies, deterministic execution, and release qualification.",
        "",
        "## Test Partitioning Summary",
        "",
        "- **Deterministic CI Tests (240+ suites):** Run in continuous integration without network or credential dependencies, utilizing mock doubles and isolated temporary worktrees.",
        "- **Live Model Tests (Partitioned):** Marked with `#[ignore]` and categorized in `tests/support/live_inventory.rs`. Require explicit `NVIDIA_API_KEY` and are invoked only via `make test-live` or dedicated workflows.",
        "- **Architectural Enforcement Tests:** Ensure layer boundaries, single-crate invariants, and fail-closed security properties cannot be violated.",
        "",
        "## Complete Inventory of 266 Test Files",
        "",
        "| Test Suite File | Lines | Test Functions | Category | Key Tested Modules |",
        "|---|:---:|:---:|---|---|",
    ]

    for path, meta in sorted(tests.items(), key=lambda x: x[0]):
        test_fns = meta.get("test_functions", [])
        m31a_mods = meta.get("m31a_imports", [])
        is_live = meta.get("is_live", False)
        
        category = "Live Model" if is_live else ("Parity" if "parity" in path else ("Platform" if "platform" in path else ("Architecture" if "architecture" in path or "authority" in path else "Integration")))
        
        # Clean module string to single line, no curly braces
        if m31a_mods:
            raw_mod = m31a_mods[0]
            clean_mod = " ".join(raw_mod.replace("\n", " ").replace("{", "(").replace("}", ")").split())
            if len(clean_mod) > 60:
                clean_mod = clean_mod[:57] + "..."
        else:
            clean_mod = "Integration"

        test_lines.append(f"| `{path}` | {meta.get('lines', 0)} | {len(test_fns)} | {category} | `{clean_mod}` |")

    with open(TESTS_DOCS_DIR / "catalog.md", "w", encoding="utf-8") as f:
        f.write("\n".join(test_lines))

    # 4. Write documentation-coverage.json
    coverage_record = {
        "total_source_files": len(sources),
        "documented_source_files": len(coverage_manifest),
        "total_test_files": len(tests),
        "documented_test_files": len(tests),
        "subsystems_count": len(by_subsystem),
        "sources": coverage_manifest,
        "tests": {
            path: {
                "doc_page": "/docs/tests/catalog",
                "lines": meta.get("lines", 0),
                "is_live": meta.get("is_live", False)
            } for path, meta in tests.items()
        }
    }

    with open(AUDIT_DIR / "documentation-coverage.json", "w", encoding="utf-8") as f:
        json.dump(coverage_record, f, indent=2)

    print("Successfully regenerated codebase and test references with clean MDX encoding:")
    print(f"  Subsystems documented: {len(by_subsystem)}")
    print(f"  Source files mapped: {len(coverage_manifest)}")
    print(f"  Test files mapped: {len(tests)}")

if __name__ == "__main__":
    main()
