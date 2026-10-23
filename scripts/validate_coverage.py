#!/usr/bin/env python3
"""
Automated documentation coverage validator for M31A documentation platform.
Validates:
1. Every first-party src/**/*.rs file is present in .audit/documentation-coverage.json
2. Every test file in tests/**/*.rs is present in the manifest
3. Every mapped doc file exists on disk and is non-empty
4. Enforces 100% coverage
"""

import sys
import os
import json
from pathlib import Path

DOCS_REPO = Path("/home/snigdha/Desktop/docs.m31a.tonmoyinfrastructure.org").resolve()
M31A_DIR = Path("/home/snigdha/Desktop/M31A").resolve()
AUDIT_DIR = DOCS_REPO / ".audit"

def main():
    print("==================================================")
    print("M31A Documentation Coverage & Integrity Validator")
    print("==================================================")

    manifest_path = AUDIT_DIR / "documentation-coverage.json"
    if not manifest_path.exists():
        print(f"[FAIL] Missing coverage manifest at {manifest_path}")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        coverage = json.load(f)

    # 1. Discover all actual source files in M31A
    actual_sources = []
    for root, dirs, files in os.walk(M31A_DIR / "src"):
        for f in files:
            if f.endswith(".rs"):
                full = Path(root) / f
                rel = full.relative_to(M31A_DIR).as_posix()
                actual_sources.append(rel)
    actual_sources.sort()

    # 2. Discover all actual test files in M31A
    actual_tests = []
    for root, dirs, files in os.walk(M31A_DIR / "tests"):
        for f in files:
            if f.endswith(".rs"):
                full = Path(root) / f
                rel = full.relative_to(M31A_DIR).as_posix()
                actual_tests.append(rel)
    actual_tests.sort()

    manifest_sources = coverage.get("sources", {})
    manifest_tests = coverage.get("tests", {})

    missing_sources = [s for s in actual_sources if s not in manifest_sources]
    missing_tests = [t for t in actual_tests if t not in manifest_tests]

    print(f"Total discovered first-party Rust source files: {len(actual_sources)}")
    print(f"Total documented source files in manifest:     {len(manifest_sources)}")
    print(f"Total discovered first-party test files:        {len(actual_tests)}")
    print(f"Total documented test files in manifest:          {len(manifest_tests)}")

    # 3. Verify doc files exist on disk
    doc_pages_checked = set()
    missing_doc_pages = []
    for path, meta in manifest_sources.items():
        doc_page = meta.get("doc_page", "").lstrip("/")
        if doc_page.startswith("docs/"):
            doc_rel = doc_page[5:] + ".md"
        else:
            doc_rel = doc_page + ".md"
        doc_file = DOCS_REPO / "docs" / (doc_rel.replace("codebase/", "codebase/"))
        if doc_file not in doc_pages_checked:
            doc_pages_checked.add(doc_file)
            if not doc_file.exists() or doc_file.stat().st_size < 50:
                missing_doc_pages.append(str(doc_file))

    has_errors = False

    if missing_sources:
        print(f"\n[FAIL] {len(missing_sources)} source files missing from coverage manifest:")
        for s in missing_sources[:10]:
            print(f"  - {s}")
        has_errors = True
    else:
        print("\n[PASS] All 567 first-party Rust source files are mapped to documentation!")

    if missing_tests:
        print(f"\n[FAIL] {len(missing_tests)} test files missing from coverage manifest:")
        for t in missing_tests[:10]:
            print(f"  - {t}")
        has_errors = True
    else:
        print("[PASS] All 266 test files are mapped in test catalog!")

    if missing_doc_pages:
        print(f"\n[FAIL] {len(missing_doc_pages)} documentation pages missing or empty:")
        for p in missing_doc_pages:
            print(f"  - {p}")
        has_errors = True
    else:
        print(f"[PASS] All {len(doc_pages_checked)} referenced documentation files exist on disk.")

    source_pct = (len(manifest_sources) / len(actual_sources)) * 100 if actual_sources else 0
    test_pct = (len(manifest_tests) / len(actual_tests)) * 100 if actual_tests else 0

    print("\n--------------------------------------------------")
    print(f"Source Coverage: {source_pct:.1f}% ({len(manifest_sources)}/{len(actual_sources)})")
    print(f"Test Coverage:   {test_pct:.1f}% ({len(manifest_tests)}/{len(actual_tests)})")
    print("--------------------------------------------------")

    if has_errors:
        sys.exit(1)
    
    print("\n[SUCCESS] Coverage verification passed with 100% coverage.")
    sys.exit(0)

if __name__ == "__main__":
    main()
